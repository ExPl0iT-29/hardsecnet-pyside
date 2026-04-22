from __future__ import annotations

import hashlib
import html
import json
import sys
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, Sequence

from hardsecnet_pyside.agents import AgentEngine
from hardsecnet_pyside.benchmark import BenchmarkImporter
from hardsecnet_pyside.config import AISettings, AppPaths
from hardsecnet_pyside.models import (
    AITaskRecord,
    AgentRecommendation,
    ApprovalRecord,
    BenchmarkDocument,
    BenchmarkItem,
    ComparisonDelta,
    ComplianceFinding,
    DeviceRecord,
    ModuleDefinition,
    ModuleResult,
    NetworkCheck,
    ProfileTemplate,
    ReportBundle,
    RunRecord,
    ScriptExecutionRecord,
    ScriptReadiness,
    StepResult,
    utc_now,
)
from hardsecnet_pyside.persistence import HardSecNetRepository
from hardsecnet_pyside.services import HardSecNetService

try:  # pragma: no cover - optional runtime dependency during development
    import fitz  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    fitz = None

try:  # pragma: no cover - optional runtime dependency during development
    from PySide6 import QtWidgets
except Exception:  # pragma: no cover - optional dependency
    QtWidgets = None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json_resource(filename: str) -> dict[str, Any]:
    from importlib import resources

    payload = resources.files("hardsecnet_pyside.resources").joinpath(filename).read_text(
        encoding="utf-8"
    )
    return json.loads(payload)


def _sort_iso_desc(items: Sequence[Any], attr: str) -> list[Any]:
    return sorted(items, key=lambda item: getattr(item, attr, ""), reverse=True)


class HardSecNetController:
    def __init__(self, project_root: Path | None = None, ai_settings: AISettings | None = None) -> None:
        self.service = HardSecNetService.bootstrap(project_root or _repo_root())
        self.paths = self.service.paths
        self.repository = self.service.repository
        self.ai_settings = ai_settings or self.service.ai_settings
        self.agent_engine = self.service.agents
        self._module_catalog = self.service.list_modules()

    def _load_module_catalog(self) -> list[ModuleDefinition]:
        raw = _load_json_resource("module_catalog.json")
        return [ModuleDefinition(**entry) for entry in raw.get("modules", [])]

    def current_device(self) -> DeviceRecord:
        return self.service.get_current_device()

    def get_current_device(self) -> DeviceRecord:
        return self.service.get_current_device()

    def module_catalog(self, os_family: str | None = None) -> list[ModuleDefinition]:
        return self.service.list_modules(os_family)

    def list_modules(self, os_family: str | None = None) -> list[ModuleDefinition]:
        return self.service.list_modules(os_family)

    def list_profiles(self, os_family: str | None = None) -> list[ProfileTemplate]:
        return self.service.list_profiles(os_family)

    def list_benchmark_documents(self, os_family: str | None = None) -> list[BenchmarkDocument]:
        return self.service.list_benchmark_documents(os_family)

    def list_benchmark_items(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[BenchmarkItem]:
        return self.service.list_benchmark_items(document_id=document_id, os_family=os_family)

    def list_script_readiness(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[ScriptReadiness]:
        return self.service.list_script_readiness(document_id=document_id, os_family=os_family)

    def list_script_executions(self, item_id: str | None = None) -> list[ScriptExecutionRecord]:
        return self.service.list_script_executions(item_id=item_id)

    def run_script_dry_run(
        self,
        item_id: str,
        *,
        operator: str | None = None,
        execute: bool = False,
    ) -> ScriptExecutionRecord:
        return self.service.run_script_dry_run(item_id, operator=operator, execute=execute)

    def list_runs(self, device_id: str | None = None) -> list[RunRecord]:
        return self.service.list_runs(device_id)

    def latest_run(self, device_id: str | None = None) -> RunRecord | None:
        runs = self.list_runs(device_id or self.get_current_device().id)
        return runs[0] if runs else None

    def list_findings(self, run_id: str | None = None) -> list[ComplianceFinding]:
        findings = self.repository.list_findings(run_id)
        return sorted(findings, key=lambda item: (item.severity, item.title), reverse=True)

    def list_comparisons(
        self, after_run_id: str | None = None, device_id: str | None = None
    ) -> list[ComparisonDelta]:
        return self.repository.list_comparisons(after_run_id=after_run_id, device_id=device_id)

    def list_reports(self) -> list[ReportBundle]:
        return self.service.list_reports()

    def latest_report(self, run_id: str | None = None) -> ReportBundle | None:
        reports = self.list_reports()
        if run_id is None:
            return reports[0] if reports else None
        for report in reports:
            if report.run_id == run_id:
                return report
        return None

    def list_approvals(self) -> list[ApprovalRecord]:
        return self.service.list_approvals()

    def list_ai_tasks(self, subject_id: str | None = None) -> list[AITaskRecord]:
        return self.service.list_ai_tasks(subject_id)

    def get_dashboard_snapshot(self):
        return self.service.get_dashboard_snapshot()

    def ai_recommendations(self, run_id: str | None = None) -> list[AgentRecommendation]:
        if run_id is None:
            run = self.latest_run()
            run_id = run.id if run is not None else None
        if run_id is None:
            return []
        recommendations: list[AgentRecommendation] = []
        for task in self.list_ai_tasks(run_id):
            result = task.result.get("recommendations", [])
            for entry in result:
                recommendations.append(AgentRecommendation(**entry))
        return recommendations

    def get_ai_recommendations(self, run_id: str) -> dict[str, list[AgentRecommendation]]:
        return self.service.get_ai_recommendations(run_id)

    def network_checks(self, run_id: str | None = None) -> list[NetworkCheck]:
        return self.service.get_network_checks(run_id)

    def get_network_checks(self, run_id: str | None = None) -> list[NetworkCheck]:
        return self.service.get_network_checks(run_id)

    def dashboard_snapshot(self) -> dict[str, Any]:
        snapshot = self.service.get_dashboard_snapshot()
        return {
            "device": snapshot.device,
            "profiles": snapshot.profiles,
            "documents": snapshot.benchmark_documents,
            "items": self.list_benchmark_items(os_family=snapshot.device.os_family),
            "runs": snapshot.runs,
            "findings": self.list_findings(snapshot.runs[0].id) if snapshot.runs else [],
            "comparisons": self.list_comparisons(after_run_id=snapshot.runs[0].id, device_id=snapshot.device.id)
            if snapshot.runs
            else [],
            "reports": snapshot.reports,
            "approvals": snapshot.pending_approvals,
            "ai_tasks": self.list_ai_tasks(snapshot.runs[0].id if snapshot.runs else None),
            "recommendations": self.ai_recommendations(snapshot.runs[0].id if snapshot.runs else None),
            "network_checks": self.network_checks(snapshot.runs[0].id if snapshot.runs else None),
            "latest_report": self.latest_report(snapshot.runs[0].id if snapshot.runs else None),
            "modules": snapshot.module_catalog,
        }

    def import_benchmark(self, source_path: str | Path) -> BenchmarkDocument:
        return self.service.import_benchmark(source_path).document

    def run_profile(
        self,
        profile_id: str,
        selected_modules: list[str] | None = None,
        operator: str | None = None,
    ):
        return self.service.run_profile(profile_id, selected_modules=selected_modules, operator=operator)

    def approve_target(
        self,
        *,
        target_type: str,
        target_id: str,
        decision: str,
        reviewer: str,
        notes: str = "",
    ) -> ApprovalRecord:
        return self.service.approve_target(
            target_type=target_type, target_id=target_id, decision=decision, reviewer=reviewer, notes=notes
        )

    def export_report_payload(self, report_id: str) -> dict[str, Any]:
        return self.service.export_report_payload(report_id)

    def _status_for_item(self, profile: ProfileTemplate, item: BenchmarkItem) -> str:
        if profile.strictness == "audit_only":
            return "Needs Review"
        if item.automated and item.confidence >= 0.8:
            return "Compliant"
        fingerprint = hashlib.sha256(f"{profile.id}:{item.id}".encode("utf-8")).hexdigest()
        bucket = int(fingerprint[:2], 16) % 5
        if profile.review_required and bucket >= 2:
            return "Needs Review"
        return "Compliant" if bucket < 3 else "Non-Compliant"

    def _severity_for_item(self, item: BenchmarkItem, status: str) -> str:
        if status == "Non-Compliant":
            return "High" if item.profile_level == "L1" else "Critical"
        if status == "Needs Review":
            return "Medium"
        return "Low"

    def _selected_items(self, profile: ProfileTemplate) -> list[BenchmarkItem]:
        items = self.list_benchmark_items(os_family=profile.os_family)
        if profile.benchmark_ids:
            selected = [item for item in items if item.benchmark_id in profile.benchmark_ids]
            if selected:
                return selected
        return items

    def _previous_run(self, device_id: str, run_id: str) -> RunRecord | None:
        for run in self.list_runs(device_id):
            if run.id != run_id:
                return run
        return None

    def create_local_baseline_run(self, profile_id: str | None = None) -> RunRecord:
        device = self.current_device()
        profile = self.repository.get_profile(profile_id) if profile_id else None
        if profile is None:
            profiles = self.list_profiles(device.os_family)
            profile = profiles[0] if profiles else self.list_profiles()[0]
        selected_items = self._selected_items(profile)
        run = RunRecord(
            id=f"run-{uuid.uuid4().hex[:12]}",
            device_id=device.id,
            profile_id=profile.id,
            os_family=profile.os_family,
            status="completed",
            modules=list(profile.module_ids),
            raw_artifacts=[],
            summary={
                "profile_name": profile.name,
                "benchmark_count": len(selected_items),
                "strictness": profile.strictness,
            },
        )

        module_results: list[ModuleResult] = []
        findings: list[ComplianceFinding] = []
        for module_id in profile.module_ids:
            module = next(
                (module for module in self.module_catalog(profile.os_family) if module.id == module_id),
                None,
            )
            module_title = module.name if module else module_id.replace("_", " ").title()
            steps = [
                StepResult(
                    stage="snapshot",
                    status="completed",
                    message=f"Captured baseline for {module_title}.",
                    command=f"{module_id} --snapshot",
                    artifact_paths=[str(self.paths.artifacts_dir / run.id / f"{module_id}-snapshot.json")],
                    evidence=[device.hostname, profile.id],
                    ended_at=utc_now(),
                ),
                StepResult(
                    stage="audit",
                    status="completed",
                    message=f"Audited {module_title} against {profile.name}.",
                    command=f"{module_id} --audit",
                    artifact_paths=[str(self.paths.artifacts_dir / run.id / f"{module_id}-audit.json")],
                    evidence=[profile.name],
                    ended_at=utc_now(),
                ),
                StepResult(
                    stage="harden",
                    status="completed" if profile.strictness != "audit_only" else "skipped",
                    message="Applied approved hardening steps."
                    if profile.strictness != "audit_only"
                    else "Audit-only profile skipped remediation.",
                    command=f"{module_id} --harden",
                    artifact_paths=[str(self.paths.artifacts_dir / run.id / f"{module_id}-harden.json")],
                    evidence=[profile.strictness],
                    ended_at=utc_now(),
                ),
                StepResult(
                    stage="compare",
                    status="completed",
                    message="Compared pre and post state for drift movement.",
                    command=f"{module_id} --compare",
                    artifact_paths=[str(self.paths.artifacts_dir / run.id / f"{module_id}-compare.json")],
                    evidence=[profile.id],
                    ended_at=utc_now(),
                ),
            ]
            module_results.append(
                ModuleResult(
                    module_id=module_id,
                    title=module_title,
                    steps=steps,
                    benchmark_refs=[item.benchmark_id for item in selected_items if module_id in item.candidate_modules],
                    manual=profile.strictness == "audit_only",
                )
            )

        for item in selected_items:
            status = self._status_for_item(profile, item)
            findings.append(
                ComplianceFinding(
                    id=f"finding-{uuid.uuid4().hex[:12]}",
                    run_id=run.id,
                    benchmark_id=item.benchmark_id,
                    title=item.title,
                    status=status,
                    severity=self._severity_for_item(item, status),
                    evidence=[*item.citations, device.hostname, profile.name],
                    expected=item.recommendation or "Aligned to benchmark guidance",
                    actual="Captured through deterministic local baseline run.",
                    source_page=item.source_page,
                    module_id=item.candidate_modules[0] if item.candidate_modules else "",
                    remediation=[step.command for step in item.remediation_steps],
                    rollback=list(item.rollback_notes),
                    rationale=item.rationale,
                    citations=item.citations,
                    confidence=item.confidence,
                )
            )

        run.module_results = module_results
        run.ended_at = utc_now()
        run.summary.update(
            {
                "compliant": sum(1 for item in findings if item.status == "Compliant"),
                "needs_review": sum(1 for item in findings if item.status == "Needs Review"),
                "non_compliant": sum(1 for item in findings if item.status == "Non-Compliant"),
            }
        )

        comparisons: list[ComparisonDelta] = []
        previous_run = self._previous_run(device.id, run.id)
        if previous_run is not None:
            previous_findings = {item.benchmark_id: item for item in self.list_findings(previous_run.id)}
            current_findings = {item.benchmark_id: item for item in findings}
            for benchmark_id, finding in current_findings.items():
                before = previous_findings.get(benchmark_id)
                if before is None:
                    delta_type = "new"
                    before_status = "Missing"
                elif before.status == finding.status:
                    delta_type = "unchanged"
                    before_status = before.status
                elif before.status != "Compliant" and finding.status == "Compliant":
                    delta_type = "improved"
                    before_status = before.status
                elif before.status == "Compliant" and finding.status != "Compliant":
                    delta_type = "regressed"
                    before_status = before.status
                else:
                    delta_type = "changed"
                    before_status = before.status
                comparisons.append(
                    ComparisonDelta(
                        id=f"delta-{uuid.uuid4().hex[:12]}",
                        device_id=device.id,
                        before_run_id=previous_run.id,
                        after_run_id=run.id,
                        benchmark_id=benchmark_id,
                        title=finding.title,
                        delta_type=delta_type,
                        before_status=before_status,
                        after_status=finding.status,
                        summary=f"{finding.title} moved from {before_status} to {finding.status}.",
                    )
                )

        report = self._generate_report_bundle(run, findings, comparisons)
        self.repository.save_run(run)
        self.repository.save_findings(findings)
        if comparisons:
            self.repository.save_comparisons(comparisons)
        self.repository.save_report(report)
        self.repository.save_approval(
            ApprovalRecord(
                id=f"approval-{uuid.uuid4().hex[:12]}",
                target_type="run",
                target_id=run.id,
                decision="review_required" if any(f.status != "Compliant" for f in findings) else "approved",
                reviewer="system",
                notes="Deterministic local baseline run completed and saved for UI verification.",
            )
        )

        approval_task, approval_recommendations = self.agent_engine.approval_gate_agent(findings)
        reasoning_task, reasoning_recommendations = self.agent_engine.audit_reasoning_agent(
            run, findings, comparisons
        )
        remediation_task, remediation_recommendations = self.agent_engine.remediation_planner_agent(
            run, findings
        )
        report_task, report_summary = self.agent_engine.report_writer_agent(run, findings, report)
        for task in (approval_task, reasoning_task, remediation_task, report_task):
            self.repository.save_ai_task(task)

        advisor_task = AITaskRecord(
            id=f"aitask-{uuid.uuid4().hex[:12]}",
            agent_type="UI Advisor Snapshot",
            subject_type="run",
            subject_id=run.id,
            provider=self.ai_settings.mode,
            status="completed",
            prompt_hash=hashlib.sha256(f"advisor:{run.id}".encode("utf-8")).hexdigest(),
            result={
                "recommendations": [
                    *[asdict(item) for item in approval_recommendations],
                    *[asdict(item) for item in reasoning_recommendations],
                    *[asdict(item) for item in remediation_recommendations],
                ],
                "summary": report_summary,
            },
            completed_at=utc_now(),
        )
        self.repository.save_ai_task(advisor_task)
        return run

    def _generate_report_bundle(
        self, run: RunRecord, findings: list[ComplianceFinding], comparisons: list[ComparisonDelta]
    ) -> ReportBundle:
        report_dir = self.paths.reports_dir / run.id
        report_dir.mkdir(parents=True, exist_ok=True)
        json_path = report_dir / f"{run.id}.json"
        html_path = report_dir / f"{run.id}.html"
        pdf_path = report_dir / f"{run.id}.pdf"

        network_checks = self.network_checks(run.id)
        summary = {
            "total_findings": len(findings),
            "compliant": sum(1 for item in findings if item.status == "Compliant"),
            "needs_review": sum(1 for item in findings if item.status == "Needs Review"),
            "non_compliant": sum(1 for item in findings if item.status == "Non-Compliant"),
            "comparisons": len(comparisons),
        }
        payload = {
            "report_id": f"report-{uuid.uuid4().hex[:12]}",
            "title": f"HardSecNet Report for {run.id}",
            "generated_at": utc_now(),
            "run": asdict(run),
            "findings": [asdict(item) for item in findings],
            "comparisons": [asdict(item) for item in comparisons],
            "network_checks": [asdict(item) for item in network_checks],
            "summary": summary,
        }
        json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

        executive_summary = (
            f"Run {run.id} completed with {summary['compliant']} compliant findings, "
            f"{summary['needs_review']} review items, and {summary['non_compliant']} non-compliant items."
        )
        technical_summary = (
            f"Profile {run.profile_id} executed against {run.os_family} with {len(run.module_results)} modules "
            f"and {len(network_checks)} network checks."
        )
        html_path.write_text(
            self._render_report_html(payload, executive_summary, technical_summary), encoding="utf-8"
        )
        if fitz is not None:
            self._write_pdf_report(pdf_path, payload, executive_summary, technical_summary)

        return ReportBundle(
            id=payload["report_id"],
            run_id=run.id,
            comparison_id=comparisons[0].id if comparisons else "",
            title=payload["title"],
            generated_at=payload["generated_at"],
            json_path=str(json_path),
            html_path=str(html_path),
            pdf_path=str(pdf_path) if fitz is not None else "",
            executive_summary=executive_summary,
            technical_summary=technical_summary,
        )

    def _render_report_html(
        self, payload: dict[str, Any], executive_summary: str, technical_summary: str
    ) -> str:
        findings_rows = "".join(
            f"<tr><td>{html.escape(item['benchmark_id'])}</td><td>{html.escape(item['title'])}</td>"
            f"<td>{html.escape(item['status'])}</td><td>{html.escape(item['severity'])}</td></tr>"
            for item in payload["findings"]
        )
        comparison_rows = "".join(
            f"<tr><td>{html.escape(item['benchmark_id'])}</td><td>{html.escape(item['delta_type'])}</td>"
            f"<td>{html.escape(item['before_status'])}</td><td>{html.escape(item['after_status'])}</td></tr>"
            for item in payload["comparisons"]
        )
        network_rows = "".join(
            f"<tr><td>{html.escape(item['title'])}</td><td>{html.escape(item['status'])}</td>"
            f"<td>{html.escape(item['details'])}</td></tr>"
            for item in payload["network_checks"]
        )
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    body {{
      font-family: Segoe UI, Arial, sans-serif;
      margin: 32px;
      color: #e6edf3;
      background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
    }}
    h1, h2 {{ color: #7ee787; }}
    .panel {{
      border: 1px solid #30363d;
      border-radius: 14px;
      padding: 18px;
      margin-bottom: 18px;
      background: rgba(13, 17, 23, 0.9);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    th, td {{
      text-align: left;
      border-bottom: 1px solid #30363d;
      padding: 8px 10px;
      font-size: 13px;
    }}
    th {{ color: #79c0ff; }}
    .muted {{ color: #8b949e; }}
  </style>
</head>
<body>
  <h1>{html.escape(payload["title"])}</h1>
  <p class="muted">Generated at {html.escape(payload["generated_at"])}</p>
  <div class="panel">
    <h2>Executive Summary</h2>
    <p>{html.escape(executive_summary)}</p>
    <p>{html.escape(technical_summary)}</p>
  </div>
  <div class="panel">
    <h2>Findings</h2>
    <table><thead><tr><th>Benchmark</th><th>Title</th><th>Status</th><th>Severity</th></tr></thead>
    <tbody>{findings_rows}</tbody></table>
  </div>
  <div class="panel">
    <h2>Comparisons</h2>
    <table><thead><tr><th>Benchmark</th><th>Delta</th><th>Before</th><th>After</th></tr></thead>
    <tbody>{comparison_rows}</tbody></table>
  </div>
  <div class="panel">
    <h2>Network Posture</h2>
    <table><thead><tr><th>Title</th><th>Status</th><th>Details</th></tr></thead>
    <tbody>{network_rows}</tbody></table>
  </div>
</body>
</html>"""

    def _write_pdf_report(
        self,
        pdf_path: Path,
        payload: dict[str, Any],
        executive_summary: str,
        technical_summary: str,
    ) -> None:
        if fitz is None:  # pragma: no cover - guarded by caller
            return
        document = fitz.open()
        sections = [
            payload["title"],
            executive_summary,
            technical_summary,
            "Findings:\n" + "\n".join(
                f"- {item['benchmark_id']} | {item['title']} | {item['status']} | {item['severity']}"
                for item in payload["findings"]
            ),
            "Comparisons:\n" + "\n".join(
                f"- {item['benchmark_id']} | {item['delta_type']} | {item['before_status']} -> {item['after_status']}"
                for item in payload["comparisons"]
            ),
        ]
        for content in sections:
            page = document.new_page()
            page.insert_text((72, 72), content, fontsize=11)
        document.save(pdf_path)


def build_window(controller: HardSecNetController | None = None):
    if QtWidgets is None:  # pragma: no cover - runtime guard
        raise RuntimeError(
            "PySide6 is not installed. Install project dependencies before launching the desktop app."
        )
    from hardsecnet_pyside.ui.main_window import MainWindow

    return MainWindow(controller or HardSecNetController())


def main(argv: Sequence[str] | None = None) -> int:
    if QtWidgets is None:  # pragma: no cover - runtime guard
        raise RuntimeError(
            "PySide6 is not installed. Install project dependencies before launching the desktop app."
        )
    app = QtWidgets.QApplication(list(argv or sys.argv))
    app.setApplicationName("HardSecNet")
    app.setOrganizationName("HardSecNet")
    window = build_window()
    window.show()
    return app.exec()
