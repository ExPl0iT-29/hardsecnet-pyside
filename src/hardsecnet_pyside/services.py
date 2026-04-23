from __future__ import annotations

import json
import os
import platform
import subprocess
import uuid
from dataclasses import asdict, dataclass
from importlib import resources
from pathlib import Path
from typing import Any

from hardsecnet_pyside.agents import AgentEngine
from hardsecnet_pyside.benchmark import BenchmarkImporter
from hardsecnet_pyside.config import AISettings, AppPaths
from hardsecnet_pyside.models import (
    AgentRecommendation,
    ApprovalRecord,
    BenchmarkDocument,
    BenchmarkItem,
    ComparisonDelta,
    ComplianceFinding,
    DeviceRecord,
    EvidenceField,
    ModuleDefinition,
    NetworkCheck,
    ProfileTemplate,
    RemediationStep,
    ReportBundle,
    RunRecord,
    ScriptExecutionRecord,
    ScriptReadiness,
    StepResult,
    ModuleResult,
    utc_now,
    to_json,
)
from hardsecnet_pyside.persistence import HardSecNetRepository


@dataclass(slots=True)
class ImportedBenchmarkResult:
    document: BenchmarkDocument
    items: list[BenchmarkItem]
    candidate_profiles: list[ProfileTemplate]
    ai_recommendations: list[AgentRecommendation]


@dataclass(slots=True)
class RunExecutionResult:
    run: RunRecord
    findings: list[ComplianceFinding]
    comparisons: list[ComparisonDelta]
    report: ReportBundle
    reasoning: list[AgentRecommendation]
    remediation_plan: list[AgentRecommendation]
    approval_review: list[AgentRecommendation]
    network_checks: list[NetworkCheck]


@dataclass(slots=True)
class DashboardSnapshot:
    device: DeviceRecord
    profiles: list[ProfileTemplate]
    benchmark_documents: list[BenchmarkDocument]
    runs: list[RunRecord]
    reports: list[ReportBundle]
    pending_approvals: list[ApprovalRecord]
    ai_tasks_count: int
    module_catalog: list[ModuleDefinition]


SCRIPT_REVIEW_MARKERS = (
    "todo",
    "manual review required",
    "convert the remediation",
    "<approved",
    "review_required",
    "replace the commented",
)
HIGH_RISK_SCRIPT_MARKERS = (
    "remove-item -recurse",
    "rm -rf",
    "set-executionpolicy",
    "format-volume",
    "reg delete",
    "del /f",
    "userdel",
    "net user /delete",
    "netsh advfirewall set allprofiles state off",
    "shutdown",
    "restart-computer",
)
MEDIUM_RISK_SCRIPT_MARKERS = (
    "set-itemproperty",
    "new-itemproperty",
    "net accounts",
    "secedit",
    "auditpol",
    "modprobe",
    "rmmod",
    "systemctl",
    "sysctl",
    "chmod",
    "chown",
)
SCRIPT_SCAFFOLD_LINES = {
    "$erroractionpreference = 'stop'",
    "set -euo pipefail",
    "set -e",
}


class HardSecNetService:
    def __init__(
        self,
        *,
        paths: AppPaths,
        repository: HardSecNetRepository,
        importer: BenchmarkImporter,
        agents: AgentEngine,
        ai_settings: AISettings,
    ) -> None:
        self.paths = paths
        self.repository = repository
        self.importer = importer
        self.agents = agents
        self.ai_settings = ai_settings
        self._module_catalog = self._load_module_catalog()

    @classmethod
    def bootstrap(cls, project_root: Path | None = None) -> "HardSecNetService":
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        paths = AppPaths.discover(project_root)
        paths.ensure()
        repository = HardSecNetRepository(paths.database_path)
        repository.initialize()
        repository.bootstrap(paths)
        service = cls(
            paths=paths,
            repository=repository,
            importer=BenchmarkImporter(),
            agents=AgentEngine(AISettings.from_env()),
            ai_settings=AISettings.from_env(),
        )
        service._ensure_default_settings()
        service._ensure_exported_benchmark_bundles()
        service._ensure_demo_ready_windows_controls()
        service._ensure_curated_script_candidates()
        service._sync_benchmark_item_script_states()
        service._ensure_benchmark_profile_templates()
        return service

    def _ensure_demo_ready_windows_controls(self) -> None:
        document = self.repository.get_benchmark_document("builtin-doc-windows")
        if document is None:
            document = BenchmarkDocument(
                id="builtin-doc-windows",
                name="Built-in Windows Desktop Baseline",
                version="1.0",
                os_family="windows",
                source_type="curated",
                source_path="built-in",
                source_hash="builtin-windows",
                status="approved",
                provenance={"origin": "hardsecnet-pyside seed data"},
            )
            self.repository.save_benchmark_document(document)

        specs = [
            (
                "builtin-item-win-file-ext",
                "CIS-Windows-Demo-FileExtensions",
                "Show file extensions",
                "Visible extensions help users and administrators identify disguised executable files.",
                "HKCU Explorer Advanced HideFileExt should be 0.",
                "Set HideFileExt to 0.",
                "Set HideFileExt back to 1 for demo rollback.",
                ["attachment-safety", "workstation-hardening", "demo-ready"],
            ),
            (
                "builtin-item-win-autorun",
                "CIS-Windows-Demo-Autorun",
                "Disable AutoRun for removable media",
                "Disabling AutoRun reduces automatic execution risk from removable drives.",
                "HKCU Explorer policy NoDriveTypeAutoRun should be 255.",
                "Set NoDriveTypeAutoRun to 255.",
                "Set NoDriveTypeAutoRun to 145 for demo rollback.",
                ["removable-media", "workstation-hardening", "demo-ready"],
            ),
            (
                "builtin-item-win-zone-info",
                "CIS-Windows-Demo-ZoneInformation",
                "Preserve downloaded-file zone information",
                "Preserving attachment origin metadata allows Windows to warn about downloaded files.",
                "HKCU Attachments SaveZoneInformation should be 2.",
                "Set SaveZoneInformation to 2.",
                "Set SaveZoneInformation to 1 for demo rollback.",
                ["attachment-safety", "workstation-hardening", "demo-ready"],
            ),
            (
                "builtin-item-win-screen-active",
                "CIS-Windows-Demo-ScreenSaverActive",
                "Enable screen saver after inactivity",
                "An active screen saver provides an inactivity trigger for session locking.",
                "HKCU Control Panel Desktop ScreenSaveActive should be 1.",
                "Set ScreenSaveActive to 1.",
                "Set ScreenSaveActive back to 0 for demo rollback.",
                ["session-security", "demo-ready"],
            ),
            (
                "builtin-item-win-screen-timeout",
                "CIS-Windows-Demo-ScreenSaverTimeout",
                "Set a short inactivity timeout",
                "A short timeout reduces the exposure window for an unattended unlocked session.",
                "HKCU Control Panel Desktop ScreenSaveTimeOut should be 60.",
                "Set ScreenSaveTimeOut to 60.",
                "Set ScreenSaveTimeOut to 600 for demo rollback.",
                ["session-security", "demo-ready"],
            ),
            (
                "builtin-item-win-password-policy",
                "CIS-Windows-Workstation-PasswordPolicy",
                "Review local password policy",
                "Password age, length, and history policy reduce weak or stale local credentials.",
                "Local password policy should align with the selected CIS account policy controls.",
                "Review with net accounts; apply through approved administrative policy tooling.",
                "Rollback through the same administrative policy tooling after approval.",
                ["password-policy", "workstation-hardening", "admin-review"],
            ),
            (
                "builtin-item-win-firewall-policy",
                "CIS-Windows-Workstation-FirewallPolicy",
                "Review Windows Defender Firewall profile policy",
                "Firewall profiles reduce unsolicited inbound network exposure on workstation devices.",
                "Domain, private, and public firewall profiles should be enabled and centrally reviewed.",
                "Review with Get-NetFirewallProfile; apply through approved administrative policy tooling.",
                "Rollback through the same administrative policy tooling after approval.",
                ["firewall", "workstation-hardening", "admin-review"],
            ),
        ]
        items: list[BenchmarkItem] = []
        for item_id, benchmark_id, title, rationale, recommendation, command, rollback, tags in specs:
            items.append(
                BenchmarkItem(
                    id=item_id,
                    document_id=document.id,
                    benchmark_id=benchmark_id,
                    title=title,
                    os_family="windows",
                    profile_level="L1",
                    automated=True,
                    rationale=rationale,
                    recommendation=recommendation,
                    remediation_steps=[
                        RemediationStep(
                            title=title,
                            command=command,
                            expected_impact=rationale,
                            rollback=rollback,
                            approval_required=True,
                        )
                    ],
                    rollback_notes=[rollback],
                    evidence_fields=[
                        EvidenceField(
                            name=benchmark_id,
                            description="Registry status emitted by the curated demo-ready script.",
                        )
                    ],
                    citations=[benchmark_id],
                    confidence=0.95,
                    status="approved",
                    tags=tags,
                    candidate_modules=["cis_audit", "baseline_harden", "drift_check"],
                )
            )
        if items:
            self.repository.save_benchmark_items(items)

    def _ensure_default_settings(self) -> None:
        defaults = {
            "report_format": "html,pdf,json",
            "operator_name": platform.node() or "operator",
            "bmadv6.enabledModules": "core,bmm,bmb,cis",
            "bmadv6.projectMode": "upstream-bmad-v6",
            "bmadv6.migrationStatus": "preflight-required",
        }
        for key, value in defaults.items():
            if not self.repository.get_setting(key):
                self.repository.set_setting(key, value)

    def _ensure_exported_benchmark_bundles(self) -> None:
        discovery = self.importer.discover_exported_bundles(self.paths.benchmark_exports_dir)
        for warning in discovery.warnings:
            self.repository.set_setting(f"benchmark_bundle_warning.{abs(hash(warning))}", warning)
        loaded_count = 0
        refreshed_count = 0
        for bundle in discovery.bundles:
            existing_document = self.repository.get_benchmark_document(bundle.document.id)
            self.repository.save_benchmark_document(bundle.document)
            self.repository.save_benchmark_items(bundle.items)
            if existing_document is None:
                loaded_count += 1
            else:
                refreshed_count += 1
            for warning in bundle.warnings:
                self.repository.set_setting(f"benchmark_bundle_warning.{abs(hash(warning))}", warning)
        self.repository.set_setting("benchmark_bundle_autoload_count", str(loaded_count))
        self.repository.set_setting("benchmark_bundle_refresh_count", str(refreshed_count))

    def _ensure_curated_script_candidates(self) -> None:
        script_dir = self.paths.generated_scripts_dir / "curated_ready"
        script_dir.mkdir(parents=True, exist_ok=True)
        curated_scripts = {
            "builtin-item-win-lock": (
                "cis-windows-lock-screen.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Control Panel\\Desktop"
$Name = "ScreenSaverIsSecure"
$ActiveName = "ScreenSaveActive"
$TimeoutName = "ScreenSaveTimeOut"
$Value = "1"
function Get-HardSecNetLockScreenState {
    if (-not (Test-Path $Path)) {
        return [pscustomobject]@{ Raw = "<missing>"; Active = "<missing>"; Timeout = "<missing>"; Enabled = $false }
    }
    $Property = Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue
    if ($null -eq $Property -or $null -eq $Property.$Name) {
        return [pscustomobject]@{ Raw = "<not configured>"; Active = "<unknown>"; Timeout = "<unknown>"; Enabled = $false }
    }
    $Active = (Get-ItemProperty -Path $Path -Name $ActiveName -ErrorAction SilentlyContinue).$ActiveName
    $Timeout = (Get-ItemProperty -Path $Path -Name $TimeoutName -ErrorAction SilentlyContinue).$TimeoutName
    return [pscustomobject]@{ Raw = $Property.$Name; Active = $Active; Timeout = $Timeout; Enabled = ([string]$Property.$Name -eq "1") }
}
function Write-HardSecNetLockScreenStatus {
    $State = Get-HardSecNetLockScreenState
    $Label = if ($State.Enabled) { "ON" } else { "OFF" }
    Write-Output "Setting: Windows secure screen saver lock"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current secure value: $($State.Raw)"
    Write-Output "Screen saver active: $($State.Active)"
    Write-Output "Timeout seconds: $($State.Timeout)"
    Write-Output "Status: $Label"
    Write-Output "Benefit: requires the user's password after inactivity, reducing unattended-session access risk."
}
if ($Status) {
    Write-HardSecNetLockScreenStatus
} elseif ($Rollback) {
    if (-not (Test-Path $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
    Set-ItemProperty -Path $Path -Name $Name -Value "0"
    Set-ItemProperty -Path $Path -Name $ActiveName -Value "1"
    Set-ItemProperty -Path $Path -Name $TimeoutName -Value "60"
    Write-Output "Dehardened demo state: secure screen saver lock is OFF with $Name=0"
    Write-HardSecNetLockScreenStatus
} elseif ($Apply) {
    if (-not (Test-Path $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
    Set-ItemProperty -Path $Path -Name $Name -Value $Value
    Set-ItemProperty -Path $Path -Name $ActiveName -Value "1"
    Set-ItemProperty -Path $Path -Name $TimeoutName -Value "60"
    Write-Output "Applied secure screen saver baseline: $Name=$Value"
    Write-HardSecNetLockScreenStatus
} else {
    Write-Output "Dry run: would ensure $Path has $Name=$Value; rollback demo would set $Name=1"
    Write-HardSecNetLockScreenStatus
}
""",
            ),
            "builtin-item-win-file-ext": (
                "cis-windows-show-file-extensions.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced"
$Name = "HideFileExt"
function Write-State {
    $Raw = (Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue).$Name
    if ($null -eq $Raw) { $Raw = "<not configured>" }
    $On = ([string]$Raw -eq "0")
    Write-Output "Setting: Show file extensions"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current value: $Raw"
    Write-Output ("Status: " + $(if ($On) { "ON" } else { "OFF" }))
    Write-Output "Benefit: makes disguised executables easier to spot, for example invoice.pdf.exe."
}
if ($Status) { Write-State }
elseif ($Rollback) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 1
    Write-Output "Dehardened demo state: file extensions are hidden."
    Write-State
}
elseif ($Apply) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 0
    Write-Output "Applied baseline: file extensions are visible."
    Write-State
}
else { Write-Output "Dry run: would set $Name=0"; Write-State }
""",
            ),
            "builtin-item-win-screen-active": (
                "cis-windows-screen-saver-active.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Control Panel\\Desktop"
$Name = "ScreenSaveActive"
function Write-State {
    $Raw = (Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue).$Name
    if ($null -eq $Raw) { $Raw = "<not configured>" }
    $On = ([string]$Raw -eq "1")
    Write-Output "Setting: Screen saver activation"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current value: $Raw"
    Write-Output ("Status: " + $(if ($On) { "ON" } else { "OFF" }))
    Write-Output "Benefit: creates an inactivity trigger so the session can lock automatically."
}
if ($Status) { Write-State }
elseif ($Rollback) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value "0"
    Write-Output "Dehardened demo state: screen saver activation is OFF."
    Write-State
}
elseif ($Apply) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value "1"
    Write-Output "Applied baseline: screen saver activation is ON."
    Write-State
}
else { Write-Output "Dry run: would set $Name=1"; Write-State }
""",
            ),
            "builtin-item-win-screen-timeout": (
                "cis-windows-screen-saver-timeout.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Control Panel\\Desktop"
$Name = "ScreenSaveTimeOut"
function Write-State {
    $Raw = (Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue).$Name
    if ($null -eq $Raw) { $Raw = "<not configured>" }
    $Parsed = 999999
    [void][int]::TryParse([string]$Raw, [ref]$Parsed)
    $On = ($Parsed -le 60)
    Write-Output "Setting: Inactivity timeout"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current value: $Raw seconds"
    Write-Output ("Status: " + $(if ($On) { "ON" } else { "OFF" }))
    Write-Output "Benefit: shortens the time an unattended session remains exposed."
}
if ($Status) { Write-State }
elseif ($Rollback) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value "600"
    Write-Output "Dehardened demo state: inactivity timeout relaxed to 600 seconds."
    Write-State
}
elseif ($Apply) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value "60"
    Write-Output "Applied baseline: inactivity timeout set to 60 seconds."
    Write-State
}
else { Write-Output "Dry run: would set $Name=60"; Write-State }
""",
            ),
            "builtin-item-win-autorun": (
                "cis-windows-disable-autorun.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer"
$Name = "NoDriveTypeAutoRun"
function Write-State {
    $Raw = (Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue).$Name
    if ($null -eq $Raw) { $Raw = "<not configured>" }
    $On = ([string]$Raw -eq "255")
    Write-Output "Setting: Disable AutoRun for removable media"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current value: $Raw"
    Write-Output ("Status: " + $(if ($On) { "ON" } else { "OFF" }))
    Write-Output "Benefit: reduces automatic execution risk from USB/removable drives."
}
if ($Status) { Write-State }
elseif ($Rollback) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 145
    Write-Output "Dehardened demo state: AutoRun policy returned to a permissive demo value."
    Write-State
}
elseif ($Apply) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 255
    Write-Output "Applied baseline: AutoRun is disabled for all drive types."
    Write-State
}
else { Write-Output "Dry run: would set $Name=255"; Write-State }
""",
            ),
            "builtin-item-win-zone-info": (
                "cis-windows-preserve-zone-info.ps1",
                """param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"
$Path = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Attachments"
$Name = "SaveZoneInformation"
function Write-State {
    $Raw = (Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue).$Name
    if ($null -eq $Raw) { $Raw = "<not configured>" }
    $On = ([string]$Raw -eq "2")
    Write-Output "Setting: Preserve downloaded-file zone information"
    Write-Output "Registry: $Path\\$Name"
    Write-Output "Current value: $Raw"
    Write-Output ("Status: " + $(if ($On) { "ON" } else { "OFF" }))
    Write-Output "Benefit: keeps origin metadata so Windows can warn about downloaded files."
}
if ($Status) { Write-State }
elseif ($Rollback) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 1
    Write-Output "Dehardened demo state: zone information preservation is disabled."
    Write-State
}
elseif ($Apply) {
    New-Item -Path $Path -Force | Out-Null
    Set-ItemProperty -Path $Path -Name $Name -Value 2
    Write-Output "Applied baseline: downloaded-file zone information is preserved."
    Write-State
}
else { Write-Output "Dry run: would set $Name=2"; Write-State }
""",
            ),
            "builtin-item-linux-ufw": (
                "cis-ubuntu-ufw-default-deny.sh",
                """#!/usr/bin/env bash
set -euo pipefail
if [ "${HARDSECNET_APPLY:-0}" = "1" ]; then
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw --force enable
  echo "Applied UFW default deny baseline"
else
  echo "Dry run: would set UFW incoming deny, outgoing allow, and enable UFW"
fi
""",
            ),
            "builtin-item-linux-gdm": (
                "cis-ubuntu-gdm-automount-disable.sh",
                """#!/usr/bin/env bash
set -euo pipefail
TARGET="/etc/dconf/db/local.d/00-media-automount"
if [ "${HARDSECNET_APPLY:-0}" = "1" ]; then
  sudo install -d -m 0755 /etc/dconf/db/local.d
  printf '%s\n' '[org/gnome/desktop/media-handling]' 'automount=false' 'automount-open=false' | sudo tee "$TARGET" >/dev/null
  sudo dconf update
  echo "Applied GDM automount disable baseline"
else
  echo "Dry run: would write $TARGET and run dconf update"
fi
""",
            ),
        }

        items = self.repository.list_benchmark_items()
        updated: list[BenchmarkItem] = []
        for item in items:
            candidate = curated_scripts.get(item.id)
            if candidate is None:
                continue
            filename, content = candidate
            script_path = script_dir / filename
            if not script_path.exists() or script_path.read_text(encoding="utf-8") != content:
                script_path.write_text(content, encoding="utf-8")
            item.script_path = str(script_path)
            item.script_state = "ready"
            note = "Curated ready script candidate bundled for local-only validation and approval-gated execution."
            item.review_notes = [entry for entry in item.review_notes if "Curated ready script candidate" not in entry]
            item.review_notes.append(note)
            updated.append(item)

        if updated:
            self.repository.save_benchmark_items(updated)
            self.repository.set_setting("curated_ready_script_count", str(len(updated)))

    def _ensure_benchmark_profile_templates(self) -> None:
        self._ensure_windows_benchmark_profile_templates()
        self._ensure_ubuntu_benchmark_profile_templates()

    def _sync_benchmark_item_script_states(self) -> None:
        items = self.repository.list_benchmark_items()
        updated: list[BenchmarkItem] = []
        for item in items:
            if not item.script_path:
                continue
            readiness = self.classify_script_item(item)
            desired_state = (
                "ready"
                if readiness.status == "ready"
                else "review_required" if readiness.status == "review_required" else item.script_state
            )
            desired_note = (
                "Reviewed script candidate converted into executable logic and validated for controlled execution."
                if readiness.status == "ready"
                else ""
            )
            changed = False
            if desired_state != item.script_state:
                item.script_state = desired_state
                changed = True
            if desired_note:
                filtered = [
                    note
                    for note in item.review_notes
                    if "Reviewed script candidate converted into executable logic" not in note
                ]
                if desired_note not in filtered:
                    filtered.append(desired_note)
                if filtered != item.review_notes:
                    item.review_notes = filtered
                    changed = True
            if changed:
                updated.append(item)
        if updated:
            self.repository.save_benchmark_items(updated)

    def _ensure_windows_benchmark_profile_templates(self) -> None:
        windows_documents = [
            document
            for document in self.list_benchmark_documents("windows")
            if document.id == "doc-0bec44c02877"
            or (
                document.name == "CIS Microsoft Windows 11 Stand-alone Benchmark"
                and document.version == "v4.0.0"
            )
        ]
        windows_documents.sort(key=lambda document: 0 if document.id == "doc-0bec44c02877" else 1)
        windows_items = (
            self.list_benchmark_items(document_id=windows_documents[0].id)
            if windows_documents
            else self.list_benchmark_items(os_family="windows")
        )
        if not windows_items:
            return

        def ids_for_prefix(prefix: str) -> list[str]:
            return [item.benchmark_id for item in windows_items if item.benchmark_id.startswith(prefix)]

        workstation_ready_ids = [
            "CIS-Windows-11-1.4.1",
            "CIS-Windows-Demo-FileExtensions",
            "CIS-Windows-Demo-Autorun",
            "CIS-Windows-Demo-ZoneInformation",
            "CIS-Windows-Demo-ScreenSaverActive",
            "CIS-Windows-Demo-ScreenSaverTimeout",
        ]
        workstation_review_ids = [
            "CIS-Windows-Workstation-PasswordPolicy",
            "CIS-Windows-Workstation-FirewallPolicy",
        ]
        workstation_benchmark_ids = [
            *workstation_ready_ids,
            *workstation_review_ids,
            *ids_for_prefix("1."),
            *ids_for_prefix("9."),
            *ids_for_prefix("17."),
            *ids_for_prefix("18.3."),
            *ids_for_prefix("18.5."),
            *ids_for_prefix("18.9."),
        ]
        password_lock_profile_ids = [
            "1.1.1",
            "1.1.2",
            "1.1.3",
            "1.1.4",
            "1.1.5",
            "1.1.6",
            "1.1.7",
            "1.2.1",
            "1.2.2",
            "1.2.4",
            "CIS-Windows-11-1.4.1",
            "CIS-Windows-Demo-ScreenSaverActive",
            "CIS-Windows-Demo-ScreenSaverTimeout",
        ]
        public_firewall_profile_ids = [
            "9.3.1",
            "9.3.2",
            "9.3.3",
            "9.3.4",
            "9.3.5",
            "9.3.6",
            "9.3.7",
            "9.3.8",
            "9.3.9",
            "17.7.4",
        ]
        dual_firewall_on_ids = [
            "9.2.1",
            "9.3.1",
        ]
        password_expiry_public_firewall_ids = [
            "1.1.2",
            *public_firewall_profile_ids,
        ]
        usb_attachment_profile_ids = [
            "CIS-Windows-Demo-FileExtensions",
            "CIS-Windows-Demo-Autorun",
            "CIS-Windows-Demo-ZoneInformation",
            "19.7.5.1",
            "19.7.5.2",
            "19.7.46.2.1",
            "18.9.52",
        ]
        workstation_essentials_ids = [
            *password_lock_profile_ids,
            *public_firewall_profile_ids,
            "17.1.1",
            "17.5.4",
            "17.5.5",
            "17.9.5",
            "19.7.40.1",
            "19.7.8.4",
        ]

        profile_specs = [
            (
                "demo_windows_workstation_hardening",
                "Windows Workstation Hardening",
                "Workstation baseline covering live reversible settings plus CIS account, firewall, audit, and administrative-template controls.",
                workstation_benchmark_ids,
                "balanced",
                True,
            ),
            (
                "demo_windows_session_security",
                "Windows Session Security",
                "Focused profile for inactivity lock and user session protection.",
                ["CIS-Windows-11-1.4.1"],
                "balanced",
                False,
            ),
            (
                "demo_windows_inactivity_lock",
                "Windows Inactivity Lock",
                "Focused profile for automatic inactivity locking behavior.",
                ["CIS-Windows-Demo-ScreenSaverActive", "CIS-Windows-Demo-ScreenSaverTimeout"],
                "balanced",
                False,
            ),
            (
                "demo_windows_removable_media_safety",
                "Windows Removable Media Safety",
                "Focused profile for AutoRun/removable-media risk reduction.",
                ["CIS-Windows-Demo-Autorun", "CIS-Windows-Demo-ZoneInformation", "CIS-Windows-Demo-FileExtensions"],
                "balanced",
                False,
            ),
            (
                "demo_windows_password_and_locking",
                "Password And Locking",
                "Demo profile for password history, complexity, lockout policy, and session-lock behavior.",
                password_lock_profile_ids,
                "balanced",
                False,
            ),
            (
                "demo_windows_public_network_lockdown",
                "Public Network Lockdown",
                "Demo profile for public firewall enforcement, restrictive inbound behavior, and firewall logging.",
                public_firewall_profile_ids,
                "strict",
                False,
            ),
            (
                "demo_windows_private_public_firewall_on",
                "Private And Public Firewall On",
                "Minimal demo profile containing only the CIS controls that ensure the private and public firewall profiles are turned on.",
                dual_firewall_on_ids,
                "balanced",
                False,
            ),
            (
                "demo_windows_password_expiry_public_firewall",
                "Password Expiry And Public Firewall",
                "Focused demo profile combining the password maximum age control with the public firewall lockdown baseline.",
                password_expiry_public_firewall_ids,
                "balanced",
                False,
            ),
            (
                "demo_windows_usb_and_attachment_safety",
                "USB And Attachment Safety",
                "Demo profile for removable-media risk, attachment origin metadata, codec download blocking, and visible file extensions.",
                usb_attachment_profile_ids,
                "balanced",
                False,
            ),
            (
                "demo_windows_workstation_essentials",
                "Workstation Essentials",
                "Balanced demo profile combining password policy, session locking, public firewall, attachment safety, and key audit signals.",
                workstation_essentials_ids,
                "balanced",
                False,
            ),
            (
                "cis_windows_11_full_benchmark",
                "CIS Windows 11 Full Benchmark",
                "All extracted Windows 11 CIS controls from the imported benchmark PDF.",
                [item.benchmark_id for item in windows_items],
                "strict",
                True,
            ),
            (
                "cis_windows_11_account_policies",
                "CIS Windows 11 Account Policies",
                "Password and account lockout policy controls from CIS section 1.",
                ids_for_prefix("1."),
                "balanced",
                True,
            ),
            (
                "cis_windows_11_local_policies",
                "CIS Windows 11 Local Policies",
                "Local policy, user rights, and security option controls from CIS section 2.",
                ids_for_prefix("2."),
                "balanced",
                True,
            ),
            (
                "cis_windows_11_firewall",
                "CIS Windows 11 Firewall",
                "Windows Defender Firewall controls from CIS section 9.",
                ids_for_prefix("9."),
                "balanced",
                True,
            ),
            (
                "cis_windows_11_audit_policy",
                "CIS Windows 11 Audit Policy",
                "Advanced audit policy controls from CIS section 17.",
                ids_for_prefix("17."),
                "audit_only",
                False,
            ),
            (
                "cis_windows_11_admin_templates",
                "CIS Windows 11 Administrative Templates",
                "Administrative template and security policy controls from CIS sections 18 and 19.",
                [*ids_for_prefix("18."), *ids_for_prefix("19.")],
                "balanced",
                True,
            ),
        ]
        modules = [module.id for module in self.list_modules("windows") if module.default_enabled]
        saved = 0
        for profile_id, name, description, benchmark_ids, strictness, review_required in profile_specs:
            if not benchmark_ids:
                continue
            self.repository.save_profile(
                ProfileTemplate(
                    id=profile_id,
                    name=name,
                    os_family="windows",
                    description=description,
                    benchmark_ids=list(dict.fromkeys(benchmark_ids)),
                    module_ids=modules,
                    strictness=strictness,
                    built_in=True,
                    review_required=review_required,
                )
            )
            saved += 1
        self.repository.set_setting("windows_benchmark_profile_count", str(saved))

    def _ensure_ubuntu_benchmark_profile_templates(self) -> None:
        ubuntu_documents = [
            document
            for document in self.list_benchmark_documents("linux")
            if document.id == "doc-d0e7eed31013"
            or (
                document.name == "CIS Ubuntu Linux 24.04 LTS Benchmark"
                and document.version == "v1.0.0"
            )
        ]
        ubuntu_documents.sort(key=lambda document: 0 if document.id == "doc-d0e7eed31013" else 1)
        ubuntu_items = (
            self.list_benchmark_items(document_id=ubuntu_documents[0].id)
            if ubuntu_documents
            else self.list_benchmark_items(os_family="linux")
        )
        if not ubuntu_items:
            return

        def ids_for_prefix(prefix: str) -> list[str]:
            return [item.benchmark_id for item in ubuntu_items if item.benchmark_id.startswith(prefix)]

        profile_specs = [
            (
                "cis_ubuntu_2404_full_benchmark",
                "CIS Ubuntu 24.04 Full Benchmark",
                "All extracted Ubuntu 24.04 CIS controls from the imported benchmark PDF.",
                [item.benchmark_id for item in ubuntu_items],
                "strict",
                True,
            ),
            (
                "cis_ubuntu_2404_initial_setup",
                "CIS Ubuntu 24.04 Initial Setup",
                "Filesystem, bootloader, package, update, and login-warning controls from CIS section 1.",
                ids_for_prefix("1."),
                "balanced",
                True,
            ),
            (
                "cis_ubuntu_2404_services",
                "CIS Ubuntu 24.04 Services",
                "Service, package, time sync, and job scheduler controls from CIS section 2.",
                ids_for_prefix("2."),
                "balanced",
                True,
            ),
            (
                "cis_ubuntu_2404_network",
                "CIS Ubuntu 24.04 Network",
                "Network kernel, firewall, nftables, iptables, and UFW controls from CIS sections 3 and 4.",
                [*ids_for_prefix("3."), *ids_for_prefix("4.")],
                "balanced",
                True,
            ),
            (
                "cis_ubuntu_2404_access_auth",
                "CIS Ubuntu 24.04 Access And Authentication",
                "SSH, privilege escalation, PAM, password, and account controls from CIS section 5.",
                ids_for_prefix("5."),
                "balanced",
                True,
            ),
            (
                "cis_ubuntu_2404_logging_audit",
                "CIS Ubuntu 24.04 Logging And Audit",
                "System logging, auditd, and log file controls from CIS section 6.",
                ids_for_prefix("6."),
                "audit_only",
                False,
            ),
            (
                "cis_ubuntu_2404_system_maintenance",
                "CIS Ubuntu 24.04 System Maintenance",
                "System file permission, user, group, and maintenance controls from CIS section 7.",
                ids_for_prefix("7."),
                "balanced",
                True,
            ),
        ]
        modules = [module.id for module in self.list_modules("linux") if module.default_enabled]
        saved = 0
        for profile_id, name, description, benchmark_ids, strictness, review_required in profile_specs:
            if not benchmark_ids:
                continue
            self.repository.save_profile(
                ProfileTemplate(
                    id=profile_id,
                    name=name,
                    os_family="linux",
                    description=description,
                    benchmark_ids=list(dict.fromkeys(benchmark_ids)),
                    module_ids=modules,
                    strictness=strictness,
                    built_in=True,
                    review_required=review_required,
                )
            )
            saved += 1
        self.repository.set_setting("ubuntu_benchmark_profile_count", str(saved))

    def _load_module_catalog(self) -> list[ModuleDefinition]:
        payload = json.loads(
            resources.files("hardsecnet_pyside.resources")
            .joinpath("module_catalog.json")
            .read_text(encoding="utf-8")
        )
        return [ModuleDefinition(**entry) for entry in payload.get("modules", [])]

    def get_current_device(self) -> DeviceRecord:
        device_id = self.repository.get_setting("current_device_id")
        device = self.repository.get_device(device_id)
        if device is None:
            raise RuntimeError("Current device is not bootstrapped.")
        return device

    def current_device(self) -> DeviceRecord:
        return self.get_current_device()

    def list_devices(self) -> list[DeviceRecord]:
        return sorted(self.repository.list_devices(), key=lambda item: (item.os_family, item.name, item.id))

    def add_local_device(
        self,
        *,
        name: str,
        os_family: str,
        hostname: str,
        make_current: bool = True,
    ) -> DeviceRecord:
        normalized_os = os_family.strip().lower()
        if normalized_os not in {"windows", "linux"}:
            raise ValueError("Device OS must be windows or linux.")
        device = DeviceRecord(
            id=f"device-{uuid.uuid4().hex[:12]}",
            name=name.strip() or f"{normalized_os.title()} Device",
            os_family=normalized_os,
            hostname=hostname.strip() or "localhost",
            metadata={"managed_by": "hardsecnet-pyside", "source": "manual"},
        )
        self.repository.save_device(device)
        if make_current:
            self.repository.set_setting("current_device_id", device.id)
        return device

    def set_current_device(self, device_id: str) -> DeviceRecord:
        device = self.repository.get_device(device_id)
        if device is None:
            raise ValueError(f"Unknown device: {device_id}")
        self.repository.set_setting("current_device_id", device.id)
        return device

    def list_modules(self, os_family: str | None = None) -> list[ModuleDefinition]:
        if not os_family:
            return list(self._module_catalog)
        lowered = os_family.lower()
        return [module for module in self._module_catalog if lowered in {family.lower() for family in module.os_families}]

    def load_modules(self, os_family: str | None = None) -> list[ModuleDefinition]:
        return self.list_modules(os_family)

    def list_profiles(self, os_family: str | None = None) -> list[ProfileTemplate]:
        profiles = self.repository.list_profiles(os_family=os_family)
        profiles = [profile for profile in profiles if not self._hide_from_demo_profile_list(profile)]
        return sorted(profiles, key=lambda item: (item.os_family, item.name))

    def load_profiles(self, os_family: str | None = None) -> list[ProfileTemplate]:
        return self.list_profiles(os_family)

    def _hide_from_demo_profile_list(self, profile: ProfileTemplate) -> bool:
        if profile.os_family not in {"windows", "linux"}:
            return False
        legacy_ids = {"default_windows_desktop", "strict_candidate", "default_ubuntu_desktop"}
        legacy_ids.update(
            {
                "demo_windows_file_attachment_safety",
            }
        )
        if profile.id in legacy_ids:
            return True
        return (
            profile.id.startswith("profile-doc-")
            and profile.name
            in {
                "CIS Microsoft Windows 11 Stand-alone Benchmark Imported Baseline",
                "CIS Ubuntu Linux 24.04 LTS Benchmark Imported Baseline",
            }
        )

    def list_benchmark_documents(self, os_family: str | None = None) -> list[BenchmarkDocument]:
        documents = self.repository.list_benchmark_documents()
        if os_family:
            documents = [document for document in documents if document.os_family == os_family]
        documents = [document for document in documents if not self._hide_from_demo_document_list(document)]
        return sorted(documents, key=lambda item: (item.os_family, item.name, item.version, item.id))

    def load_benchmark_documents(self, os_family: str | None = None) -> list[BenchmarkDocument]:
        return self.list_benchmark_documents(os_family)

    def _hide_from_demo_document_list(self, document: BenchmarkDocument) -> bool:
        canonical_windows = {
            "name": "CIS Microsoft Windows 11 Stand-alone Benchmark",
            "version": "v4.0.0",
            "keep_id": "doc-0bec44c02877",
        }
        canonical_ubuntu = {
            "name": "CIS Ubuntu Linux 24.04 LTS Benchmark",
            "version": "v1.0.0",
            "keep_id": "doc-d0e7eed31013",
        }
        if (
            document.os_family == "windows"
            and document.name == canonical_windows["name"]
            and document.version == canonical_windows["version"]
            and document.id != canonical_windows["keep_id"]
        ):
            return True
        if (
            document.os_family == "linux"
            and document.name == canonical_ubuntu["name"]
            and document.version == canonical_ubuntu["version"]
            and document.id != canonical_ubuntu["keep_id"]
        ):
            return True
        return False

    def list_benchmark_items(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[BenchmarkItem]:
        items = self.repository.list_benchmark_items(document_id=document_id, os_family=os_family)
        if document_id is None:
            hidden_document_ids = {
                document.id
                for document in self.repository.list_benchmark_documents()
                if self._hide_from_demo_document_list(document)
            }
            if hidden_document_ids:
                items = [item for item in items if item.document_id not in hidden_document_ids]
        return sorted(items, key=lambda item: item.benchmark_id)

    def load_benchmark_items(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[BenchmarkItem]:
        return self.list_benchmark_items(document_id=document_id, os_family=os_family)

    def list_script_readiness(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[ScriptReadiness]:
        return [
            self.classify_script_item(item)
            for item in self.list_benchmark_items(document_id=document_id, os_family=os_family)
        ]

    def list_script_executions(self, item_id: str | None = None) -> list[ScriptExecutionRecord]:
        executions = self.repository.list_script_executions(item_id=item_id)
        return sorted(executions, key=lambda item: (item.created_at, item.id), reverse=True)

    def classify_script_item(self, item: BenchmarkItem) -> ScriptReadiness:
        script_path = self._resolve_script_path(item)
        if script_path is None:
            return ScriptReadiness(
                item_id=item.id,
                document_id=item.document_id,
                benchmark_id=item.benchmark_id,
                title=item.title,
                os_family=item.os_family,
                script_path=item.script_path,
                status="missing",
                reason="No generated script candidate is available for this benchmark control.",
                risk_level="unknown",
                rollback_notes=list(item.rollback_notes),
                review_notes=list(item.review_notes),
            )

        content = script_path.read_text(encoding="utf-8", errors="replace")
        lowered = content.lower()
        commands = self._script_command_preview(content)
        risk_level = self._script_risk_level(lowered)
        review_reasons = [marker for marker in SCRIPT_REVIEW_MARKERS if marker in lowered]
        if review_reasons:
            status = "review_required"
            reason = f"Script contains review marker: {review_reasons[0]}."
        elif not commands:
            status = "review_required"
            reason = "Script has no actionable command lines beyond comments or scaffolding."
        else:
            status = "ready"
            reason = "Script candidate has actionable commands and no review marker."

        if risk_level == "high" and status == "ready":
            status = "review_required"
            reason = "High-risk command pattern requires operator review before execution."

        return ScriptReadiness(
            item_id=item.id,
            document_id=item.document_id,
            benchmark_id=item.benchmark_id,
            title=item.title,
            os_family=item.os_family,
            script_path=str(script_path),
            status=status,
            reason=reason,
            risk_level=risk_level,
            commands_preview=commands,
            rollback_notes=list(item.rollback_notes),
            review_notes=list(item.review_notes),
        )

    def run_script_dry_run(
        self,
        item_id: str,
        *,
        operator: str | None = None,
        execute: bool = False,
        rollback: bool = False,
        status_check: bool = False,
        ) -> ScriptExecutionRecord:
        item = self._get_benchmark_item(item_id)
        readiness = self.classify_script_item(item)
        requires_admin_for_status = self._script_requires_admin_for_status(readiness)
        requires_admin_for_mutation = self._script_requires_admin_for_mutation(readiness)
        is_elevated = self._session_is_elevated(item.os_family)
        allow_execute = os.getenv("HARDSECNET_ALLOW_SCRIPT_EXECUTION") == "1"
        mode = "status" if status_check else "rollback" if rollback else "execute" if execute else "dry_run"
        command = self._script_execution_command(
            item,
            readiness,
            execute=execute,
            rollback=rollback,
            status_check=status_check,
        )
        execution_id = f"script-{uuid.uuid4().hex[:12]}"
        execution = ScriptExecutionRecord(
            id=execution_id,
            benchmark_item_id=item.id,
            benchmark_id=item.benchmark_id,
            document_id=item.document_id,
            mode=mode,
            status="blocked",
            command=command,
            operator=operator or self.repository.get_setting("operator_name", "operator"),
            allow_execute=allow_execute,
            readiness_status=readiness.status,
            risk_level=readiness.risk_level,
        )

        if readiness.status == "missing":
            execution.error = readiness.reason
        elif status_check and readiness.status != "ready":
            execution.error = f"Status check blocked because readiness is {readiness.status}."
        elif status_check and requires_admin_for_status and not is_elevated:
            execution.error = (
                "This script requires an elevated Administrator session. "
                "Relaunch the app from an elevated terminal to check or apply this control."
            )
        elif (execute or rollback) and requires_admin_for_mutation and not is_elevated:
            execution.error = (
                "This script requires an elevated Administrator session. "
                "Relaunch the app from an elevated terminal to check or apply this control."
            )
        elif status_check:
            execution.status, execution.output, execution.error = self._execute_script_command(
                command,
                status_check=True,
            )
        elif (execute or rollback) and not allow_execute:
            execution.error = "Live script execution is disabled. Set HARDSECNET_ALLOW_SCRIPT_EXECUTION=1 to enable it."
        elif (execute or rollback) and readiness.status != "ready":
            execution.error = f"Script execution blocked because readiness is {readiness.status}."
        elif execute or rollback:
            execution.status, execution.output, execution.error = self._execute_script_command(command)
        else:
            execution.status = "dry_run_recorded"
            execution.output = (
                "Dry run recorded. No system changes were made. "
                f"Readiness={readiness.status}; risk={readiness.risk_level}."
            )

        execution.completed_at = utc_now()
        artifact_path = self._write_script_execution_artifact(execution, readiness)
        execution.artifact_path = str(artifact_path)
        artifact_path.write_text(
            to_json(
                {
                    "execution": asdict(execution),
                    "readiness": asdict(readiness),
                    "recorded_at": utc_now(),
                }
            ),
            encoding="utf-8",
        )
        self.repository.save_script_execution(execution)
        return execution

    def _script_requires_admin_for_status(self, readiness: ScriptReadiness) -> bool:
        if not readiness.script_path:
            return False
        script_path = Path(readiness.script_path)
        if not script_path.exists():
            return False
        try:
            content = script_path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            return False
        admin_markers = (
            "auditpol",
            "secedit",
            "net accounts",
        )
        return any(marker in content for marker in admin_markers)

    def _script_requires_admin_for_mutation(self, readiness: ScriptReadiness) -> bool:
        if not readiness.script_path:
            return False
        script_path = Path(readiness.script_path)
        if not script_path.exists():
            return False
        try:
            content = script_path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            return False
        admin_markers = (
            "auditpol",
            "secedit",
            "net accounts",
            "hklm:\\",
            "hkey_local_machine",
            "new-itemproperty",
            "set-itemproperty",
            "remove-itemproperty",
            "set-netfirewallprofile",
        )
        return any(marker in content for marker in admin_markers)

    def _session_is_elevated(self, os_family: str) -> bool:
        if os_family != "windows":
            return True
        try:
            completed = subprocess.run(
                "powershell -NoProfile -Command \"[bool](([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))\"",
                capture_output=True,
                shell=True,
                text=True,
                timeout=10,
                cwd=str(self.paths.project_root),
            )
        except (OSError, subprocess.SubprocessError):
            return False
        return completed.returncode == 0 and completed.stdout.strip().lower() == "true"

    def list_runs(self, device_id: str | None = None) -> list[RunRecord]:
        runs = self.repository.list_runs(device_id=device_id)
        return sorted(runs, key=lambda item: (item.started_at, item.id), reverse=True)

    def list_reports(self) -> list[ReportBundle]:
        reports = self.repository.list_reports()
        return sorted(reports, key=lambda item: (item.generated_at, item.id), reverse=True)

    def list_comparisons(
        self, after_run_id: str | None = None, device_id: str | None = None
    ) -> list[ComparisonDelta]:
        comparisons = self.repository.list_comparisons(
            after_run_id=after_run_id, device_id=device_id
        )
        return sorted(comparisons, key=lambda item: (item.after_run_id, item.id), reverse=True)

    def list_approvals(self) -> list[ApprovalRecord]:
        approvals = self.repository.list_approvals()
        return sorted(approvals, key=lambda item: (item.decided_at, item.id), reverse=True)

    def list_ai_tasks(self, subject_id: str | None = None) -> list[Any]:
        tasks = self.repository.list_ai_tasks(subject_id=subject_id)
        return sorted(tasks, key=lambda item: (item.created_at, item.id), reverse=True)

    def get_dashboard_snapshot(self) -> DashboardSnapshot:
        device = self.get_current_device()
        return DashboardSnapshot(
            device=device,
            profiles=self.list_profiles(device.os_family),
            benchmark_documents=self.list_benchmark_documents(device.os_family),
            runs=self.list_runs(device.id),
            reports=self.list_reports(),
            pending_approvals=[
                approval for approval in self.list_approvals() if approval.decision in {"pending", "review"}
            ],
            ai_tasks_count=len(self.list_ai_tasks()),
            module_catalog=self.list_modules(device.os_family),
        )

    def import_benchmark(self, import_path: str | Path) -> ImportedBenchmarkResult:
        path = Path(import_path)
        document, items = self.importer.import_path(path)
        imported_target = self.paths.imports_dir / path.name
        imported_target.write_bytes(path.read_bytes())
        document.source_path = str(imported_target)
        generated_dir = self.paths.generated_scripts_dir / document.id
        generated_paths = self.importer.generate_script_candidates(document, items, generated_dir)
        exported_bundle = self.importer.export_benchmark_bundle(document, items, self.paths.benchmark_exports_dir)
        document.provenance["generated_script_dir"] = str(generated_dir)
        document.provenance["generated_script_count"] = len(generated_paths)
        document.provenance["generated_script_paths"] = generated_paths
        document.provenance["export_bundle_dir"] = exported_bundle["bundle_dir"]
        document.provenance["export_items_path"] = exported_bundle["items_path"]
        document.provenance["export_document_path"] = exported_bundle["document_path"]
        document.provenance["export_readme_path"] = exported_bundle["readme_path"]
        document.provenance["export_script_dir"] = exported_bundle["scripts_dir"]
        self.repository.save_benchmark_document(document)
        self.repository.save_benchmark_items(items)

        ingestion_task, recommendations = self.agents.benchmark_ingestion_agent(document, items)
        self.repository.save_ai_task(ingestion_task)

        profile_task, profiles = self.agents.profile_builder_agent(document, items)
        self.repository.save_ai_task(profile_task)
        for profile in profiles:
            self.repository.save_profile(profile)

        return ImportedBenchmarkResult(
            document=document,
            items=items,
            candidate_profiles=profiles,
            ai_recommendations=recommendations,
        )

    def run_profile(
        self,
        profile_id: str,
        selected_modules: list[str] | None = None,
        operator: str | None = None,
    ) -> RunExecutionResult:
        device = self.get_current_device()
        profile = self.repository.get_profile(profile_id)
        if profile is None:
            raise ValueError(f"Unknown profile: {profile_id}")

        modules = selected_modules or profile.module_ids
        benchmark_items = self._profile_benchmark_scope(device.os_family, profile)

        run_id = f"run-{uuid.uuid4().hex[:12]}"
        run = RunRecord(
            id=run_id,
            device_id=device.id,
            profile_id=profile.id,
            os_family=device.os_family,
            status="completed",
            modules=modules,
            summary={
                "profile_name": profile.name,
                "benchmark_scope": "profile_selected_controls" if profile.benchmark_ids else "all_available_for_device",
                "benchmark_count": len(benchmark_items),
            },
        )

        run.module_results = self._build_module_results(run, benchmark_items, modules)
        findings = self._build_findings(run, benchmark_items, profile)
        run.summary = self._summarize_findings(findings)
        run.summary.update(
            {
                "profile_name": profile.name,
                "benchmark_scope": "profile_selected_controls" if profile.benchmark_ids else "all_available_for_device",
                "benchmark_count": len(benchmark_items),
            }
        )
        run.ended_at = utc_now()

        self.repository.save_run(run)
        self.repository.save_findings(findings)

        previous_runs = [item for item in self.list_runs(device.id) if item.id != run.id]
        comparisons = self._build_comparisons(run, findings, previous_runs[:1])
        if comparisons:
            self.repository.save_comparisons(comparisons)

        report = self._build_and_store_report(run, findings, comparisons)
        reasoning_task, reasoning = self.agents.audit_reasoning_agent(run, findings, comparisons)
        remediation_task, remediation_plan = self.agents.remediation_planner_agent(run, findings)
        approval_task, approval_review = self.agents.approval_gate_agent(findings)
        report_task, generated_summary = self.agents.report_writer_agent(run, findings, report)

        report.executive_summary = generated_summary
        report.technical_summary = self._technical_summary(run, findings, comparisons)
        self._rewrite_report_artifacts(report, run, findings, comparisons)
        self.repository.save_report(report)

        for task in (reasoning_task, remediation_task, approval_task, report_task):
            self.repository.save_ai_task(task)

        approval_record = ApprovalRecord(
            id=f"approval-{uuid.uuid4().hex[:12]}",
            target_type="run",
            target_id=run.id,
            decision="review",
            reviewer=operator or self.repository.get_setting("operator_name", "operator"),
            notes="Run completed. Review remediation recommendations before hardening actions.",
        )
        self.repository.save_approval(approval_record)

        return RunExecutionResult(
            run=run,
            findings=findings,
            comparisons=comparisons,
            report=report,
            reasoning=reasoning,
            remediation_plan=remediation_plan,
            approval_review=approval_review,
            network_checks=self.get_network_checks(run.id),
        )

    def get_network_checks(self, run_id: str | None = None) -> list[NetworkCheck]:
        findings = self.repository.list_findings(run_id=run_id) if run_id else []
        if not findings and self.list_runs(self.get_current_device().id):
            latest_run = self.list_runs(self.get_current_device().id)[0]
            findings = self.repository.list_findings(run_id=latest_run.id)

        checks: list[NetworkCheck] = []
        for finding in findings:
            if "network" in finding.title.lower() or "firewall" in finding.title.lower():
                checks.append(
                    NetworkCheck(
                        id=f"net-{finding.id}",
                        title=finding.title,
                        status=finding.status,
                        details=f"Expected: {finding.expected or 'benchmark-aligned posture'} | Actual: {finding.actual or 'see run evidence'}",
                        benchmark_refs=[finding.benchmark_id],
                    )
                )
        if not checks:
            checks.append(
                NetworkCheck(
                    id="net-default",
                    title="Network posture baseline",
                    status="Review Required",
                    details="No network-specific finding has been produced yet. Run an audit profile to populate live network posture checks.",
                    benchmark_refs=[],
                )
            )
        return checks

    def get_ai_recommendations(self, run_id: str) -> dict[str, list[AgentRecommendation]]:
        run = self.repository.get_run(run_id)
        if run is None:
            raise ValueError(f"Unknown run: {run_id}")
        findings = self.repository.list_findings(run_id=run.id)
        comparisons = self.repository.list_comparisons(after_run_id=run.id)
        _, reasoning = self.agents.audit_reasoning_agent(run, findings, comparisons)
        _, remediation = self.agents.remediation_planner_agent(run, findings)
        _, approvals = self.agents.approval_gate_agent(findings)
        return {
            "reasoning": reasoning,
            "remediation": remediation,
            "approvals": approvals,
        }

    def approve_target(
        self,
        *,
        target_type: str,
        target_id: str,
        decision: str,
        reviewer: str,
        notes: str = "",
    ) -> ApprovalRecord:
        approval = ApprovalRecord(
            id=f"approval-{uuid.uuid4().hex[:12]}",
            target_type=target_type,
            target_id=target_id,
            decision=decision,
            reviewer=reviewer,
            notes=notes,
        )
        self.repository.save_approval(approval)
        return approval

    def export_report_payload(self, report_id: str) -> dict[str, Any]:
        report = self.repository.get_report(report_id)
        if report is None:
            raise ValueError(f"Unknown report: {report_id}")
        run = self.repository.get_run(report.run_id)
        if run is None:
            raise ValueError(f"Unknown run linked to report: {report.run_id}")
        payload = {
            "report": asdict(report),
            "run": asdict(run),
            "findings": [asdict(item) for item in self.repository.list_findings(run_id=run.id)],
            "comparisons": [asdict(item) for item in self.repository.list_comparisons(after_run_id=run.id)],
            "device": asdict(self.get_current_device()),
        }
        return payload

    def _build_module_results(
        self,
        run: RunRecord,
        benchmark_items: list[BenchmarkItem],
        selected_modules: list[str],
    ) -> list[ModuleResult]:
        module_index = {module.id: module for module in self._module_catalog}
        results: list[ModuleResult] = []
        artifact_dir = self.paths.artifacts_dir / run.id
        artifact_dir.mkdir(parents=True, exist_ok=True)
        for module_id in selected_modules:
            module = module_index.get(module_id)
            if module is None:
                continue
            related_items = [item for item in benchmark_items if module_id in item.candidate_modules]
            if not related_items:
                related_items = benchmark_items[:1]
            artifact_path = artifact_dir / f"{module.id}.json"
            artifact_payload = {
                "run_id": run.id,
                "module_id": module.id,
                "module_name": module.name,
                "os_family": run.os_family,
                "benchmark_refs": [item.benchmark_id for item in related_items],
                "captured_at": utc_now(),
            }
            artifact_path.write_text(to_json(artifact_payload), encoding="utf-8")
            results.append(
                ModuleResult(
                    module_id=module.id,
                    title=module.name,
                    benchmark_refs=[item.benchmark_id for item in related_items],
                    manual=module_id == "baseline_harden",
                    steps=[
                        StepResult(
                            stage="prepare",
                            status="completed",
                            message=f"Prepared {module.name} for {run.os_family}.",
                            evidence=[f"legacy_repo:{self._legacy_repo_for_os(run.os_family)}"],
                        ),
                        StepResult(
                            stage="execute",
                            status="completed",
                            message=f"Executed deterministic {module.name} scaffold flow.",
                            evidence=[item.title for item in related_items[:3]],
                        ),
                        StepResult(
                            stage="record",
                            status="completed",
                            message="Captured artifacts and traceability links.",
                            artifact_paths=[str(artifact_path)],
                        ),
                    ],
                )
            )
        return results

    def _profile_benchmark_scope(self, os_family: str, profile: ProfileTemplate) -> list[BenchmarkItem]:
        if profile.id.startswith("cis_windows_11_"):
            items = self.repository.list_benchmark_items(document_id="doc-0bec44c02877")
            if not items:
                items = self.repository.list_benchmark_items(os_family=os_family)
        elif profile.id.startswith("cis_ubuntu_2404_"):
            items = self.repository.list_benchmark_items(document_id="doc-d0e7eed31013")
            if not items:
                items = self.repository.list_benchmark_items(os_family=os_family)
        else:
            items = self.repository.list_benchmark_items(os_family=os_family)
        if not items:
            return []
        if profile.benchmark_ids:
            allowed = set(profile.benchmark_ids)
            selected = [item for item in items if item.benchmark_id in allowed]
            if selected:
                deduped: dict[str, BenchmarkItem] = {}
                for item in selected:
                    deduped.setdefault(item.benchmark_id, item)
                items = list(deduped.values())
        priority = {benchmark_id: index for index, benchmark_id in enumerate(profile.benchmark_ids)}
        return sorted(
            items,
            key=lambda item: (
                0 if item.benchmark_id in priority else 1,
                priority.get(item.benchmark_id, len(priority)),
                item.benchmark_id,
            ),
        )

    def _build_findings(
        self,
        run: RunRecord,
        benchmark_items: list[BenchmarkItem],
        profile: ProfileTemplate,
    ) -> list[ComplianceFinding]:
        findings: list[ComplianceFinding] = []
        for index, item in enumerate(benchmark_items, start=1):
            compliant = item.status == "approved" and index % 3 != 0
            status = "Compliant" if compliant else "Needs Review"
            actual = (
                "Synthetic audit confirms expected state."
                if compliant
                else "Synthetic audit flagged a variance that requires operator review."
            )
            findings.append(
                ComplianceFinding(
                    id=f"finding-{uuid.uuid4().hex[:12]}",
                    run_id=run.id,
                    benchmark_id=item.benchmark_id,
                    title=item.title,
                    status=status,
                    severity="medium" if compliant else "high",
                    evidence=[
                        f"profile:{profile.name}",
                        f"module_refs:{','.join(item.candidate_modules)}",
                        *item.citations[:2],
                    ],
                    expected=item.recommendation or "Approved benchmark-aligned state",
                    actual=actual,
                    source_page=item.source_page,
                    module_id=item.candidate_modules[0] if item.candidate_modules else "",
                    remediation=[step.command for step in item.remediation_steps],
                    rollback=item.rollback_notes or [step.rollback for step in item.remediation_steps],
                    rationale=item.rationale,
                    citations=item.citations,
                    confidence=item.confidence,
                )
            )
        return findings

    def _summarize_findings(self, findings: list[ComplianceFinding]) -> dict[str, Any]:
        compliant = sum(1 for finding in findings if finding.status == "Compliant")
        review = sum(1 for finding in findings if finding.status != "Compliant")
        return {
            "total_findings": len(findings),
            "compliant": compliant,
            "needs_review": review,
            "approval_required": review > 0,
        }

    def _build_comparisons(
        self,
        run: RunRecord,
        findings: list[ComplianceFinding],
        previous_runs: list[RunRecord],
    ) -> list[ComparisonDelta]:
        if not previous_runs:
            return []
        prior_run = previous_runs[0]
        prior_findings = {
            finding.benchmark_id: finding for finding in self.repository.list_findings(run_id=prior_run.id)
        }
        comparisons: list[ComparisonDelta] = []
        for finding in findings:
            previous = prior_findings.get(finding.benchmark_id)
            if previous is None or previous.status == finding.status:
                continue
            comparisons.append(
                ComparisonDelta(
                    id=f"cmp-{uuid.uuid4().hex[:12]}",
                    device_id=run.device_id,
                    before_run_id=prior_run.id,
                    after_run_id=run.id,
                    benchmark_id=finding.benchmark_id,
                    title=finding.title,
                    delta_type="improved" if finding.status == "Compliant" else "regressed",
                    before_status=previous.status,
                    after_status=finding.status,
                    summary=f"{finding.title}: {previous.status} -> {finding.status}",
                )
            )
        return comparisons

    def _build_and_store_report(
        self,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
    ) -> ReportBundle:
        report_id = f"report-{uuid.uuid4().hex[:12]}"
        report = ReportBundle(
            id=report_id,
            run_id=run.id,
            comparison_id=comparisons[0].id if comparisons else "",
            title=f"HardSecNet Report {run.id}",
        )
        payload = self.exportable_report_payload(run, findings, comparisons, report)
        json_path = self.paths.reports_dir / f"{report.id}.json"
        html_path = self.paths.reports_dir / f"{report.id}.html"
        pdf_path = self.paths.reports_dir / f"{report.id}.pdf"

        json_path.write_text(to_json(payload), encoding="utf-8")
        html_body = self._render_report_html(run, findings, comparisons, report)
        html_path.write_text(html_body, encoding="utf-8")
        self._write_pdf(pdf_path, run, findings, comparisons, report)

        report.json_path = str(json_path)
        report.html_path = str(html_path)
        report.pdf_path = str(pdf_path)
        report.executive_summary = self._executive_summary(run, findings)
        report.technical_summary = self._technical_summary(run, findings, comparisons)
        self.repository.save_report(report)
        return report

    def _rewrite_report_artifacts(
        self,
        report: ReportBundle,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
    ) -> None:
        if report.json_path:
            Path(report.json_path).write_text(
                to_json(self.exportable_report_payload(run, findings, comparisons, report)),
                encoding="utf-8",
            )
        if report.html_path:
            Path(report.html_path).write_text(
                self._render_report_html(run, findings, comparisons, report),
                encoding="utf-8",
            )
        if report.pdf_path:
            self._write_pdf(Path(report.pdf_path), run, findings, comparisons, report)

    def exportable_report_payload(
        self,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
        report: ReportBundle,
    ) -> dict[str, Any]:
        return {
            "report": asdict(report),
            "run": asdict(run),
            "device": asdict(self.get_current_device()),
            "findings": [asdict(item) for item in findings],
            "comparisons": [asdict(item) for item in comparisons],
            "network_checks": [asdict(item) for item in self.get_network_checks(run.id)],
            "ai_mode": self.ai_settings.mode,
            "generated_at": utc_now(),
        }

    def _get_benchmark_item(self, item_id: str) -> BenchmarkItem:
        for item in self.repository.list_benchmark_items():
            if item.id == item_id:
                return item
        raise ValueError(f"Unknown benchmark item: {item_id}")

    def _resolve_script_path(self, item: BenchmarkItem) -> Path | None:
        candidates: list[Path] = []
        if item.script_path:
            raw_path = Path(item.script_path)
            candidates.append(raw_path)
            if not raw_path.is_absolute():
                candidates.extend(
                    [
                        self.paths.project_root / raw_path,
                        self.paths.workspace_root / raw_path,
                        self.paths.benchmark_exports_dir / raw_path,
                    ]
                )
        suffix = ".ps1" if item.os_family == "windows" else ".sh"
        inferred_name = f"{item.benchmark_id}{suffix}"
        document = self.repository.get_benchmark_document(item.document_id)
        if document is not None:
            script_dir = document.provenance.get("export_script_dir") or document.provenance.get("generated_script_dir")
            if script_dir:
                candidates.append(Path(str(script_dir)) / inferred_name)
                if item.script_path:
                    candidates.append(Path(str(script_dir)) / Path(item.script_path).name)
            export_dir = document.provenance.get("export_dir")
            if export_dir:
                candidates.append(Path(str(export_dir)) / "scripts" / inferred_name)

        if not item.script_path:
            candidates.extend(
                [
                    self.paths.generated_scripts_dir / item.document_id / inferred_name,
                    self.paths.benchmark_exports_dir / inferred_name,
                ]
            )

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate
        return None

    def _script_command_preview(self, content: str) -> list[str]:
        commands: list[str] = []
        for line in content.splitlines():
            cleaned = line.strip()
            lowered = cleaned.lower()
            if not cleaned or cleaned.startswith("#") or cleaned.startswith("//"):
                continue
            if cleaned.startswith("<#") or cleaned.startswith("#>"):
                continue
            if lowered.startswith("rem "):
                continue
            if lowered in SCRIPT_SCAFFOLD_LINES or cleaned.startswith("#!"):
                continue
            commands.append(cleaned)
            if len(commands) >= 8:
                break
        return commands

    def _script_risk_level(self, lowered_content: str) -> str:
        if any(marker in lowered_content for marker in HIGH_RISK_SCRIPT_MARKERS):
            return "high"
        if any(marker in lowered_content for marker in MEDIUM_RISK_SCRIPT_MARKERS):
            return "medium"
        return "low"

    def _script_execution_command(
        self,
        item: BenchmarkItem,
        readiness: ScriptReadiness,
        *,
        execute: bool = False,
        rollback: bool = False,
        status_check: bool = False,
    ) -> str:
        if not readiness.script_path:
            return ""
        script_path = Path(readiness.script_path)
        if item.os_family == "windows" or script_path.suffix.lower() == ".ps1":
            apply_flag = " -Status" if status_check else " -Rollback" if rollback else " -Apply" if execute else ""
            return f'powershell -NoProfile -ExecutionPolicy Bypass -File "{script_path}"{apply_flag}'
        if status_check:
            return f'bash "{script_path}"'
        if rollback:
            return f'HARDSECNET_ROLLBACK=1 bash "{script_path}"'
        if execute:
            return f'HARDSECNET_APPLY=1 bash "{script_path}"'
        return f'bash "{script_path}"'

    def _execute_script_command(self, command: str, *, status_check: bool = False) -> tuple[str, str, str]:
        if not command:
            return "blocked", "", "No executable command was resolved."
        completed = subprocess.run(
            command,
            capture_output=True,
            shell=True,
            text=True,
            timeout=120,
            cwd=str(self.paths.project_root),
        )
        if status_check and completed.returncode in {0, 2}:
            status = "completed"
        else:
            status = "completed" if completed.returncode == 0 else "failed"
        return status, completed.stdout.strip(), completed.stderr.strip()

    def _write_script_execution_artifact(
        self,
        execution: ScriptExecutionRecord,
        readiness: ScriptReadiness,
    ) -> Path:
        artifact_dir = self.paths.artifacts_dir / "script_executions"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        return artifact_dir / f"{execution.id}.json"

    def _render_report_html(
        self,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
        report: ReportBundle,
    ) -> str:
        findings_markup = "\n".join(
            (
                f"<tr><td>{finding.benchmark_id}</td><td>{finding.title}</td>"
                f"<td>{finding.status}</td><td>{finding.severity}</td>"
                f"<td>{'<br/>'.join(finding.evidence)}</td></tr>"
            )
            for finding in findings
        )
        comparisons_markup = "\n".join(
            f"<li>{delta.summary}</li>" for delta in comparisons
        ) or "<li>No prior baseline available for comparison.</li>"
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>{report.title}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #102132;
      --accent: #0b6b82;
      --bg: #f5f0e8;
      --panel: #ffffff;
      --muted: #57707d;
      --line: #d4dce2;
    }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "Noto Sans", sans-serif;
      background: linear-gradient(135deg, #f5f0e8 0%, #edf7f8 100%);
      color: var(--ink);
    }}
    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px;
    }}
    section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 14px 40px rgba(16, 33, 50, 0.08);
    }}
    h1, h2 {{ margin-top: 0; }}
    h1 {{ color: var(--accent); }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    .pill {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: #e1f0f4;
      color: var(--accent);
      font-size: 12px;
      font-weight: 600;
    }}
  </style>
</head>
<body>
  <main>
    <section>
      <span class="pill">Benchmark-aware hardening report</span>
      <h1>{report.title}</h1>
      <p>{report.executive_summary or self._executive_summary(run, findings)}</p>
      <div class="meta">
        <div><strong>Run ID</strong><br />{run.id}</div>
        <div><strong>Device</strong><br />{self.get_current_device().name}</div>
        <div><strong>Profile</strong><br />{run.profile_id}</div>
        <div><strong>Generated</strong><br />{report.generated_at}</div>
      </div>
    </section>
    <section>
      <h2>Finding Summary</h2>
      <table>
        <thead>
          <tr><th>Benchmark</th><th>Title</th><th>Status</th><th>Severity</th><th>Evidence</th></tr>
        </thead>
        <tbody>
          {findings_markup}
        </tbody>
      </table>
    </section>
    <section>
      <h2>Comparison Deltas</h2>
      <ul>{comparisons_markup}</ul>
    </section>
    <section>
      <h2>Technical Summary</h2>
      <p>{report.technical_summary or self._technical_summary(run, findings, comparisons)}</p>
    </section>
  </main>
</body>
</html>
"""

    def _write_pdf(
        self,
        pdf_path: Path,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
        report: ReportBundle,
    ) -> None:
        try:
            import fitz  # type: ignore
        except ImportError:
            pdf_path.write_text(
                f"{report.title}\n\n{self._executive_summary(run, findings)}\n\n"
                f"{self._technical_summary(run, findings, comparisons)}\n",
                encoding="utf-8",
            )
            return

        document = fitz.open()
        content_lines = [
            report.title,
            "",
            f"Run ID: {run.id}",
            f"Profile: {run.profile_id}",
            f"Device: {self.get_current_device().name}",
            "",
            "Executive Summary",
            report.executive_summary or self._executive_summary(run, findings),
            "",
            "Technical Summary",
            report.technical_summary or self._technical_summary(run, findings, comparisons),
            "",
            "Findings",
        ]
        max_pdf_findings = 180
        for finding in findings[:max_pdf_findings]:
            content_lines.extend(
                [
                    f"- {finding.benchmark_id} | {finding.status} | {finding.title}",
                    f"  Expected: {finding.expected}",
                    f"  Actual: {finding.actual}",
                ]
            )
            if finding.remediation:
                content_lines.append(f"  Remediation: {finding.remediation[0][:220]}")
        if len(findings) > max_pdf_findings:
            content_lines.extend(
                [
                    "",
                    f"PDF finding list truncated at {max_pdf_findings} entries for readability.",
                    "Open the HTML or JSON report for the complete finding set.",
                ]
            )
        self._write_pdf_lines(document, content_lines)
        document.save(pdf_path)
        document.close()

    def _write_pdf_lines(self, document: Any, lines: list[str]) -> None:
        try:
            import fitz  # type: ignore
        except ImportError:  # pragma: no cover - guarded by caller
            return

        page_lines: list[str] = []
        max_lines = 42
        for line in lines:
            wrapped = self._wrap_pdf_line(line)
            for wrapped_line in wrapped:
                page_lines.append(wrapped_line)
                if len(page_lines) >= max_lines:
                    page = document.new_page()
                    page.insert_textbox(fitz.Rect(48, 48, 548, 780), "\n".join(page_lines), fontsize=10.5)
                    page_lines = []
        if page_lines or not lines:
            page = document.new_page()
            page.insert_textbox(fitz.Rect(48, 48, 548, 780), "\n".join(page_lines), fontsize=10.5)

    def _wrap_pdf_line(self, line: str, width: int = 92) -> list[str]:
        if len(line) <= width:
            return [self._pdf_safe_line(line)]
        chunks: list[str] = []
        current = self._pdf_safe_line(line)
        prefix = "  " if line.startswith("  ") else ""
        while len(current) > width:
            split_at = current.rfind(" ", 0, width)
            if split_at <= 0:
                split_at = width
            chunks.append(current[:split_at])
            current = prefix + current[split_at:].lstrip()
        chunks.append(current)
        return chunks

    def _pdf_safe_line(self, line: str) -> str:
        cleaned = line.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        return cleaned.encode("latin-1", errors="replace").decode("latin-1")[:900]

    def _executive_summary(self, run: RunRecord, findings: list[ComplianceFinding]) -> str:
        summary = self._summarize_findings(findings)
        return (
            f"Profile {run.profile_id} completed on {self.get_current_device().hostname} with "
            f"{summary['compliant']} compliant findings and {summary['needs_review']} items requiring review. "
            "All output is traceable to benchmark references, evidence, and rollback-aware remediation notes."
        )

    def _technical_summary(
        self,
        run: RunRecord,
        findings: list[ComplianceFinding],
        comparisons: list[ComparisonDelta],
    ) -> str:
        comparison_text = (
            f"{len(comparisons)} before/after deltas were recorded."
            if comparisons
            else "No prior run was available for delta analysis."
        )
        return (
            f"Run status: {run.status}. Modules executed: {', '.join(run.modules)}. "
            f"Findings generated: {len(findings)}. {comparison_text} "
            f"Artifacts were written to {self.paths.reports_dir} and {self.paths.artifacts_dir}."
        )

    def _legacy_repo_for_os(self, os_family: str) -> Path:
        return self.paths.windows_repo if os_family == "windows" else self.paths.linux_repo
