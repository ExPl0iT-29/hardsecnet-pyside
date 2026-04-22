from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from hardsecnet_pyside.benchmark import BenchmarkImporter
from hardsecnet_pyside.models import BenchmarkDocument, BenchmarkItem, CheckLogic, EvidenceField, RemediationStep
from hardsecnet_pyside.services import HardSecNetService


WINDOWS_SNIPPET = """
1.1.1 (L1) Ensure 'Password must meet complexity requirements' is set to 'Enabled' (Automated)
Profile Applicability:
Level 1 - Stand-alone
Description:
This policy setting determines whether passwords must meet complexity requirements.
Rationale:
Passwords that contain only alphanumeric characters are extremely easy to discover.
Impact:
Users may need help desk support during rollout.
Audit:
Navigate to the UI Path articulated in the Remediation section and confirm it is set as prescribed.
Remediation:
Navigate to Computer Configuration\\Policies\\Windows Settings\\Security Settings and set the policy to Enabled.
Default Value:
Disabled.
"""

UBUNTU_SNIPPET = """
3.2.1 Ensure dccp kernel module is not available (Automated)
Description:
The Datagram Congestion Control Protocol (DCCP) is a transport layer protocol.
Rationale:
If the protocol is not required, it should be disabled.
Audit:
Run the following command to verify the kernel module is not available:
modprobe -n -v dccp
Remediation:
Run the following script to unload and disable the dccp module:
- IF - the dccp kernel module is available in ANY installed kernel:
• Create a file ending in .conf with install dccp /bin/false in the /etc/modprobe.d/ directory
• Create a file ending in .conf with blacklist dccp in the /etc/modprobe.d/ directory
• Run modprobe -r dccp 2>/dev/null; rmmod dccp 2>/dev/null to remove dccp from the kernel
"""


def test_cis_parser_extracts_windows_control_sections() -> None:
    importer = BenchmarkImporter()
    controls = importer._parse_cis_pdf_controls([WINDOWS_SNIPPET])

    assert len(controls) == 1
    control = controls[0]
    assert control.benchmark_id == "1.1.1"
    assert control.profile_level == "L1"
    assert control.automated is True
    assert "Passwords that contain only alphanumeric characters" in control.sections["Rationale"]
    assert control.source_page == 1


def test_cis_parser_extracts_linux_remediation_commands() -> None:
    importer = BenchmarkImporter()
    controls = importer._parse_cis_pdf_controls([UBUNTU_SNIPPET])
    document = BenchmarkDocument(
        id="doc-test",
        name="CIS Ubuntu Linux 24.04 LTS Benchmark",
        version="v1.0.0",
        os_family="linux",
        source_type="pdf-text",
        source_path="sample.pdf",
        source_hash="hash",
    )
    item = importer._parsed_control_to_item(document, controls[0])

    assert item.benchmark_id == "3.2.1"
    assert item.automated is True
    assert "modprobe -r dccp" in item.remediation_steps[0].command
    assert "cis_audit" in item.candidate_modules


def test_import_benchmark_generates_script_candidates(tmp_path: Path) -> None:
    controller_root = tmp_path / "hardsecnet-pyside"
    service = HardSecNetService.bootstrap(project_root=controller_root)
    benchmark_path = tmp_path / "cis_ubuntu_sample.txt"
    benchmark_path.write_text(UBUNTU_SNIPPET, encoding="utf-8")

    result = service.import_benchmark(benchmark_path)

    generated_dir = Path(result.document.provenance["generated_script_dir"])
    generated_files = list(generated_dir.iterdir())
    export_bundle_dir = Path(result.document.provenance["export_bundle_dir"])
    export_items_path = Path(result.document.provenance["export_items_path"])
    export_document_path = Path(result.document.provenance["export_document_path"])
    export_script_dir = Path(result.document.provenance["export_script_dir"])
    assert result.document.provenance["generated_script_count"] == len(generated_files)
    assert generated_files
    assert generated_files[0].suffix == ".sh"
    assert "dccp" in generated_files[0].read_text(encoding="utf-8")
    assert export_bundle_dir.exists()
    assert export_items_path.exists()
    assert export_document_path.exists()
    assert export_script_dir.exists()
    assert any(path.suffix == ".sh" for path in export_script_dir.iterdir())


def _write_exported_bundle(
    export_root: Path,
    *,
    document_id: str,
    os_family: str,
    benchmark_id: str,
    with_script: bool = True,
) -> Path:
    importer = BenchmarkImporter()
    bundle_dir = export_root / f"{document_id}-bundle"
    scripts_dir = bundle_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    document = BenchmarkDocument(
        id=document_id,
        name=f"CIS {os_family.title()} Benchmark",
        version="v-test",
        os_family=os_family,
        source_type="pdf-text",
        source_path="imported.pdf",
        source_hash=f"{document_id}-hash",
        status="review_required",
    )
    item = BenchmarkItem(
        id=f"{document_id}-item",
        document_id=document.id,
        benchmark_id=benchmark_id,
        title="Ensure benchmark-native scripts are available",
        os_family=os_family,
        automated=True,
        audit_logic=[
            CheckLogic(
                kind="test",
                target=benchmark_id,
                operator="review_required",
                expected="script candidate",
                notes="test control",
            )
        ],
        remediation_steps=[
            RemediationStep(
                title="Apply test control",
                command="Write-Output test" if os_family == "windows" else "echo test",
                expected_impact="test",
                rollback="test",
            )
        ],
        evidence_fields=[EvidenceField(name="test_evidence", description="test")],
        candidate_modules=["cis_audit"],
    )
    (bundle_dir / "benchmark_document.json").write_text(
        json.dumps(asdict(document), indent=2),
        encoding="utf-8",
    )
    (bundle_dir / "benchmark_items.json").write_text(
        json.dumps([asdict(item)], indent=2),
        encoding="utf-8",
    )
    if with_script:
        extension = ".ps1" if os_family == "windows" else ".sh"
        (scripts_dir / f"{importer._slug(benchmark_id)}{extension}").write_text(
            "# generated candidate\n",
            encoding="utf-8",
        )
    return bundle_dir


def test_discover_exported_bundles_detects_valid_and_ignores_invalid(tmp_path: Path) -> None:
    export_root = tmp_path / "benchmark_exports"
    _write_exported_bundle(
        export_root,
        document_id="doc-valid-windows",
        os_family="windows",
        benchmark_id="1.1.1",
    )
    (export_root / "broken-bundle").mkdir(parents=True)

    discovery = BenchmarkImporter().discover_exported_bundles(export_root)

    assert len(discovery.bundles) == 1
    assert discovery.bundles[0].document.id == "doc-valid-windows"
    assert discovery.bundles[0].items[0].script_path.endswith("1.1.1.ps1")
    assert discovery.warnings
    assert "broken-bundle" in discovery.warnings[0]


def test_bootstrap_autoloads_exported_bundles_once(tmp_path: Path) -> None:
    project_root = tmp_path / "hardsecnet-pyside"
    export_root = project_root / "src" / "hardsecnet_pyside" / "data" / "benchmark_exports"
    _write_exported_bundle(
        export_root,
        document_id="doc-native-windows",
        os_family="windows",
        benchmark_id="1.1.1",
    )
    _write_exported_bundle(
        export_root,
        document_id="doc-native-ubuntu",
        os_family="linux",
        benchmark_id="3.2.1",
    )

    service = HardSecNetService.bootstrap(project_root=project_root)
    service = HardSecNetService.bootstrap(project_root=project_root)

    documents = service.list_benchmark_documents()
    assert len([document for document in documents if document.id == "doc-native-windows"]) == 1
    assert len([document for document in documents if document.id == "doc-native-ubuntu"]) == 1
    windows_items = service.list_benchmark_items(document_id="doc-native-windows")
    ubuntu_items = service.list_benchmark_items(document_id="doc-native-ubuntu")
    assert windows_items[0].script_path.endswith("1.1.1.ps1")
    assert windows_items[0].script_state == "candidate"
    assert ubuntu_items[0].script_path.endswith("3.2.1.sh")
    assert ubuntu_items[0].script_state == "candidate"


def test_exported_bundle_missing_script_becomes_review_issue(tmp_path: Path) -> None:
    export_root = tmp_path / "benchmark_exports"
    _write_exported_bundle(
        export_root,
        document_id="doc-missing-script",
        os_family="linux",
        benchmark_id="4.1.1",
        with_script=False,
    )

    discovery = BenchmarkImporter().discover_exported_bundles(export_root)

    item = discovery.bundles[0].items[0]
    assert item.script_path == ""
    assert item.script_state == "missing"
    assert item.review_notes
    assert discovery.bundles[0].warnings
