from __future__ import annotations

import hashlib
import html
import json
import sqlite3
import sys
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from hardsecnet_pyside.agents import AgentEngine
from hardsecnet_pyside.benchmark import BenchmarkImporter
from hardsecnet_pyside.backend_client import ControlPlaneClient
from hardsecnet_pyside.config import AISettings, AppPaths, ControlPlaneSettings
from hardsecnet_pyside.models import (
    AITaskRecord,
    AgentRecommendation,
    ApprovalRecord,
    AgentHeartbeat,
    AgentManifest,
    BenchmarkDocument,
    BenchmarkItem,
    ComparisonDelta,
    ComparisonCampaign,
    ComplianceFinding,
    DeviceRecord,
    ModuleDefinition,
    ModuleResult,
    NetworkCheck,
    ProfileTemplate,
    JobRequest,
    JobResultEnvelope,
    ReportBundle,
    RunRecord,
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


@dataclass(slots=True)
class FleetDeviceRow:
    device: DeviceRecord
    manifest: AgentManifest | None
    heartbeat_status: str
    queued_jobs: int


@dataclass(slots=True)
class FleetJobRow:
    job: JobRequest
    status: str
    claimed_at: str
    completed_at: str
    summary: str
    artifacts: list[str]


@dataclass(slots=True)
class FleetSnapshot:
    devices: list[FleetDeviceRow]
    jobs: list[FleetJobRow]
    results: list[JobResultEnvelope]
    campaigns: list[ComparisonCampaign]
    active_device_count: int
    queued_job_count: int
    completed_job_count: int


class HardSecNetController:
    def __init__(self, project_root: Path | None = None, ai_settings: AISettings | None = None) -> None:
        self.service = HardSecNetService.bootstrap(project_root or _repo_root())
        self.paths = self.service.paths
        self.repository = self.service.repository
        self.ai_settings = ai_settings or self.service.ai_settings
        self.control_plane = ControlPlaneClient(ControlPlaneSettings.from_env())
        self.agent_engine = self.service.agents
        self._module_catalog = self.service.list_modules()
        self._ensure_fleet_tables()

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

    def _ensure_fleet_tables(self) -> None:
        ddl = [
            """
            CREATE TABLE IF NOT EXISTS fleet_heartbeats (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                status TEXT NOT NULL,
                queued_jobs INTEGER NOT NULL,
                observed_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS fleet_jobs (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                approval_required INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                claimed_at TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS fleet_results (
                job_id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
        ]
        with self.repository.connect() as conn:
            for statement in ddl:
                conn.execute(statement)
            conn.commit()

    def _fleet_row(self, row: sqlite3.Row, cls: type[Any]) -> Any:
        payload = json.loads(row["payload"])
        if cls is JobRequest:
            return JobRequest(**payload)
        if cls is JobResultEnvelope:
            return JobResultEnvelope(**payload)
        if cls is AgentManifest:
            return AgentManifest(**payload)
        raise TypeError(f"Unsupported fleet payload type: {cls!r}")

    def enroll_device(
        self,
        *,
        device_id: str,
        name: str,
        os_family: str,
        hostname: str,
        agent_version: str = "1.0.0",
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentManifest:
        device = DeviceRecord(
            id=device_id,
            name=name,
            os_family=os_family,
            hostname=hostname,
            agent_mode="fleet",
            metadata=metadata or {},
        )
        self.repository.save_device(device)
        manifest = AgentManifest(
            device_id=device.id,
            agent_version=agent_version,
            capabilities=capabilities or ["audit", "compare", "report-sync"],
        )
        self.repository.save_agent_manifest(manifest)
        return manifest

    def record_heartbeat(
        self,
        *,
        device_id: str,
        status: str,
        queued_jobs: int,
    ) -> AgentHeartbeat:
        if self.repository.get_device(device_id) is None:
            raise ValueError(f"Unknown device: {device_id}")
        heartbeat = AgentHeartbeat(
            id=f"hb-{device_id}",
            device_id=device_id,
            status=status,
            queued_jobs=queued_jobs,
        )
        with self.repository.connect() as conn:
            conn.execute(
                """
                INSERT INTO fleet_heartbeats (id, device_id, status, queued_jobs, observed_at, payload)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status = excluded.status,
                    queued_jobs = excluded.queued_jobs,
                    observed_at = excluded.observed_at,
                    payload = excluded.payload
                """,
                (
                    f"hb-{device_id}",
                    heartbeat.device_id,
                    heartbeat.status,
                    heartbeat.queued_jobs,
                    heartbeat.observed_at,
                    json.dumps(asdict(heartbeat), indent=2, sort_keys=True),
                ),
            )
            conn.commit()
        self.repository.save_agent_manifest(
            AgentManifest(
                device_id=device_id,
                agent_version=self._manifest_for_device(device_id).agent_version
                if self._manifest_for_device(device_id)
                else "1.0.0",
                capabilities=self._manifest_for_device(device_id).capabilities
                if self._manifest_for_device(device_id)
                else ["audit", "compare", "report-sync"],
                last_sync=heartbeat.observed_at,
            )
        )
        return heartbeat

    def queue_job(
        self,
        *,
        device_id: str,
        action: str,
        payload: dict[str, Any],
        approval_required: bool = True,
    ) -> JobRequest:
        if self.repository.get_device(device_id) is None:
            raise ValueError(f"Unknown device: {device_id}")
        job = JobRequest(
            id=f"job-{uuid.uuid4().hex[:12]}",
            device_id=device_id,
            action=action,
            payload=payload,
            approval_required=approval_required,
        )
        with self.repository.connect() as conn:
            conn.execute(
                """
                INSERT INTO fleet_jobs (id, device_id, action, status, approval_required, created_at, claimed_at, completed_at, payload)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job.id,
                    job.device_id,
                    job.action,
                    "pending",
                    int(job.approval_required),
                    utc_now(),
                    "",
                    "",
                    json.dumps(asdict(job), indent=2, sort_keys=True),
                ),
            )
            conn.commit()
        self.record_heartbeat(
            device_id=device_id,
            status="queued",
            queued_jobs=self.count_pending_jobs(device_id=device_id),
        )
        return job

    def claim_job(self, job_id: str) -> JobRequest:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT * FROM fleet_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise ValueError(f"Unknown job: {job_id}")
            payload = json.loads(row["payload"])
            payload["id"] = row["id"]
            payload["device_id"] = row["device_id"]
            payload["action"] = row["action"]
            payload["approval_required"] = bool(row["approval_required"])
            job = JobRequest(**payload)
            conn.execute(
                """
                UPDATE fleet_jobs
                SET status = ?, claimed_at = ?, payload = ?
                WHERE id = ?
                """,
                (
                    "in_progress",
                    utc_now(),
                    json.dumps(asdict(job), indent=2, sort_keys=True),
                    job_id,
                ),
            )
            conn.commit()
        self.record_heartbeat(
            device_id=job.device_id,
            status="in_progress",
            queued_jobs=self.count_pending_jobs(device_id=job.device_id),
        )
        return job

    def complete_job(
        self,
        job_id: str,
        *,
        summary: str,
        artifacts: list[str] | None = None,
        status: str = "completed",
    ) -> JobResultEnvelope:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT * FROM fleet_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise ValueError(f"Unknown job: {job_id}")
            job_payload = json.loads(row["payload"])
            device_id = row["device_id"]
            envelope = JobResultEnvelope(
                id=f"result-{job_id}",
                job_id=job_id,
                device_id=device_id,
                status=status,
                summary=summary,
                artifacts=list(artifacts or []),
            )
            conn.execute(
                """
                UPDATE fleet_jobs
                SET status = ?, completed_at = ?, payload = ?
                WHERE id = ?
                """,
                (
                    status,
                    utc_now(),
                    json.dumps(job_payload, indent=2, sort_keys=True),
                    job_id,
                ),
            )
            conn.execute(
                """
                INSERT INTO fleet_results (job_id, device_id, status, summary, payload)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    device_id = excluded.device_id,
                    status = excluded.status,
                    summary = excluded.summary,
                    payload = excluded.payload
                """,
                (
                    envelope.job_id,
                    envelope.device_id,
                    envelope.status,
                    envelope.summary,
                    json.dumps(asdict(envelope), indent=2, sort_keys=True),
                ),
            )
            conn.commit()
        self.record_heartbeat(
            device_id=device_id,
            status=status,
            queued_jobs=self.count_pending_jobs(device_id=device_id),
        )
        return envelope

    def list_fleet_jobs(self, device_id: str | None = None) -> list[JobRequest]:
        query = "SELECT payload FROM fleet_jobs"
        params: tuple[Any, ...] = ()
        if device_id:
            query += " WHERE device_id = ?"
            params = (device_id,)
        with self.repository.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        jobs = [JobRequest(**json.loads(row["payload"])) for row in rows]
        return sorted(jobs, key=lambda item: item.id, reverse=True)

    def list_fleet_results(self, device_id: str | None = None) -> list[JobResultEnvelope]:
        query = "SELECT payload FROM fleet_results"
        params: tuple[Any, ...] = ()
        if device_id:
            query += " WHERE device_id = ?"
            params = (device_id,)
        with self.repository.connect() as conn:
            rows = conn.execute(query, params).fetchall()
        results = [JobResultEnvelope(**json.loads(row["payload"])) for row in rows]
        return sorted(results, key=lambda item: item.job_id, reverse=True)

    def list_heartbeats(self) -> list[AgentHeartbeat]:
        with self.repository.connect() as conn:
            rows = conn.execute("SELECT payload FROM fleet_heartbeats").fetchall()
        heartbeats = [AgentHeartbeat(**json.loads(row["payload"])) for row in rows]
        return sorted(heartbeats, key=lambda item: item.observed_at, reverse=True)

    def list_campaigns(self) -> list[ComparisonCampaign]:
        with self.repository.connect() as conn:
            rows = conn.execute("SELECT payload FROM comparison_campaigns").fetchall()
        campaigns = [ComparisonCampaign(**json.loads(row["payload"])) for row in rows]
        return sorted(campaigns, key=lambda item: item.created_at, reverse=True)

    def create_campaign(
        self, *, name: str, device_ids: list[str], benchmark_scope: list[str]
    ) -> ComparisonCampaign:
        campaign = ComparisonCampaign(
            id=f"camp-{uuid.uuid4().hex[:12]}",
            name=name,
            device_ids=device_ids,
            benchmark_scope=benchmark_scope,
        )
        self.repository.save_campaign(campaign)
        return campaign

    def count_pending_jobs(self, device_id: str | None = None) -> int:
        query = "SELECT COUNT(*) AS count FROM fleet_jobs WHERE status = 'pending'"
        params: tuple[Any, ...] = ()
        if device_id:
            query += " AND device_id = ?"
            params = (device_id,)
        with self.repository.connect() as conn:
            row = conn.execute(query, params).fetchone()
        return int(row["count"]) if row else 0

    def _manifest_for_device(self, device_id: str) -> AgentManifest | None:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT payload FROM agent_manifests WHERE device_id = ?", (device_id,)).fetchone()
        if row is None:
            return None
        return AgentManifest(**json.loads(row["payload"]))

    def get_fleet_snapshot(self) -> FleetSnapshot:
        devices: list[FleetDeviceRow] = []
        latest_heartbeats = {hb.device_id: hb for hb in self.list_heartbeats()}
        pending_by_device: dict[str, int] = {}
        for job in self._fleet_job_requests():
            if job.action:
                pending_by_device[job.device_id] = pending_by_device.get(job.device_id, 0) + (
                    1 if self._job_status(job.id) == "pending" else 0
                )
        for device in self.repository.list_devices():
            manifest = self._manifest_for_device(device.id)
            heartbeat = latest_heartbeats.get(device.id)
            devices.append(
                FleetDeviceRow(
                    device=device,
                    manifest=manifest,
                    heartbeat_status=heartbeat.status if heartbeat else "unknown",
                    queued_jobs=pending_by_device.get(device.id, 0),
                )
            )
        jobs = [
            FleetJobRow(
                job=job,
                status=self._job_status(job.id),
                claimed_at=self._job_claimed_at(job.id),
                completed_at=self._job_completed_at(job.id),
                summary=self._job_summary(job.id),
                artifacts=self._job_artifacts(job.id),
            )
            for job in self._fleet_job_requests()
        ]
        results = self._fleet_result_rows()
        campaigns = self._fleet_campaign_rows()
        return FleetSnapshot(
            devices=devices,
            jobs=jobs,
            results=results,
            campaigns=campaigns,
            active_device_count=len(devices),
            queued_job_count=sum(row.queued_jobs for row in devices),
            completed_job_count=len(results),
        )

    def _job_status(self, job_id: str) -> str:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT status FROM fleet_jobs WHERE id = ?", (job_id,)).fetchone()
        return str(row["status"]) if row else "unknown"

    def _fleet_job_requests(self) -> list[JobRequest]:
        with self.repository.connect() as conn:
            rows = conn.execute("SELECT payload FROM fleet_jobs").fetchall()
        jobs = [JobRequest(**json.loads(row["payload"])) for row in rows]
        return sorted(jobs, key=lambda item: item.id, reverse=True)

    def _job_claimed_at(self, job_id: str) -> str:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT claimed_at FROM fleet_jobs WHERE id = ?", (job_id,)).fetchone()
        return str(row["claimed_at"]) if row else ""

    def _job_completed_at(self, job_id: str) -> str:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT completed_at FROM fleet_jobs WHERE id = ?", (job_id,)).fetchone()
        return str(row["completed_at"]) if row else ""

    def _job_summary(self, job_id: str) -> str:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT summary FROM fleet_results WHERE job_id = ?", (job_id,)).fetchone()
        return str(row["summary"]) if row else ""

    def _job_artifacts(self, job_id: str) -> list[str]:
        with self.repository.connect() as conn:
            row = conn.execute("SELECT payload FROM fleet_results WHERE job_id = ?", (job_id,)).fetchone()
        if row is None:
            return []
        return JobResultEnvelope(**json.loads(row["payload"])).artifacts

    def _fleet_result_rows(self) -> list[JobResultEnvelope]:
        with self.repository.connect() as conn:
            rows = conn.execute("SELECT payload FROM fleet_results").fetchall()
        results = [JobResultEnvelope(**json.loads(row["payload"])) for row in rows]
        return sorted(results, key=lambda item: item.job_id, reverse=True)

    def _fleet_campaign_rows(self) -> list[ComparisonCampaign]:
        with self.repository.connect() as conn:
            rows = conn.execute("SELECT payload FROM comparison_campaigns").fetchall()
        campaigns = [ComparisonCampaign(**json.loads(row["payload"])) for row in rows]
        return sorted(campaigns, key=lambda item: item.created_at, reverse=True)

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

    def fleet_snapshot(self) -> FleetSnapshot:
        if self.control_plane.enabled:
            summary = self.control_plane.fleet_summary()
            devices = [
                FleetDeviceRow(
                    device=DeviceRecord(
                        id=row["device"]["id"],
                        name=row["device"]["name"],
                        os_family=row["device"]["os_family"],
                        hostname=row["device"]["hostname"],
                        last_seen=row["device"]["last_seen"],
                        agent_mode=row["device"].get("agent_mode", "fleet"),
                        tags=row["device"].get("tags", []),
                        metadata=row["device"].get("metadata", {}),
                    ),
                    manifest=AgentManifest(**row["manifest"]) if row.get("manifest") else None,
                    heartbeat_status=(row.get("heartbeat") or {}).get("status", "unknown"),
                    queued_jobs=row.get("pending_jobs", 0),
                )
                for row in summary.get("devices", [])
            ]
            jobs = [
                FleetJobRow(
                    job=JobRequest(**job),
                    status=job["status"],
                    claimed_at=job.get("claimed_at") or "",
                    completed_at=job.get("completed_at") or "",
                    summary=job.get("result_summary", ""),
                    artifacts=job.get("artifact_paths", []),
                )
                for job in summary.get("jobs", [])
            ]
            results = [
                JobResultEnvelope(
                    id=item["id"],
                    job_id=item.get("job_id", ""),
                    device_id=item["device_id"],
                    status="completed",
                    summary=item.get("summary", ""),
                    artifacts=[path for path in [item.get("json_path", ""), item.get("html_path", ""), item.get("pdf_path", "")] if path],
                    run_id=item.get("run_id", ""),
                )
                for item in summary.get("reports", [])
            ]
            return FleetSnapshot(
                devices=devices,
                jobs=jobs,
                results=results,
                campaigns=[ComparisonCampaign(**item) for item in summary.get("campaigns", [])],
                active_device_count=summary.get("active_device_count", len(devices)),
                queued_job_count=summary.get("queued_job_count", 0),
                completed_job_count=summary.get("completed_job_count", 0),
            )
        return self.get_fleet_snapshot()

    def enroll_fleet_device(
        self,
        *,
        device_id: str,
        name: str,
        os_family: str,
        hostname: str,
        agent_version: str = "1.0.0",
        capabilities: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AgentManifest:
        if self.control_plane.enabled:
            enrolled = self.control_plane.enroll_device(
                device_id=device_id,
                name=name,
                hostname=hostname,
                os_family=os_family,
                agent_version=agent_version,
                capabilities=capabilities or ["remote-audit", "remote-harden", "remote-compare"],
                metadata=metadata,
            )
            return AgentManifest(**enrolled["manifest"])
        return self.enroll_device(
            device_id=device_id,
            name=name,
            os_family=os_family,
            hostname=hostname,
            agent_version=agent_version,
            capabilities=capabilities,
            metadata=metadata,
        )

    def record_fleet_heartbeat(self, device_id: str, status: str, queued_jobs: int) -> AgentHeartbeat:
        if self.control_plane.enabled:
            return AgentHeartbeat(
                **self.control_plane.record_heartbeat(
                    device_id=device_id,
                    status=status,
                    queued_jobs=queued_jobs,
                )
            )
        return self.record_heartbeat(device_id=device_id, status=status, queued_jobs=queued_jobs)

    def queue_fleet_job(
        self,
        device_id: str,
        action: str,
        payload: dict[str, Any],
        approval_required: bool = True,
    ) -> JobRequest:
        if self.control_plane.enabled:
            job = self.control_plane.create_job(
                device_id=device_id,
                action=action,
                payload=payload,
                approval_required=approval_required,
            )
            if approval_required:
                job = self.control_plane.approve_job(job["id"])
            return JobRequest(**job)
        return self.queue_job(
            device_id=device_id,
            action=action,
            payload=payload,
            approval_required=approval_required,
        )

    def claim_fleet_job(self, job_id: str) -> JobRequest:
        if self.control_plane.enabled:
            return JobRequest(**self.control_plane.claim_job(job_id))
        return self.claim_job(job_id)

    def complete_fleet_job(
        self,
        job_id: str,
        *,
        summary: str,
        artifacts: list[str] | None = None,
        status: str = "completed",
    ) -> JobResultEnvelope:
        if self.control_plane.enabled:
            jobs = self.control_plane.list_jobs()
            job = next((item for item in jobs if item["id"] == job_id), None)
            if job is None:
                raise ValueError(f"Unknown remote job: {job_id}")
            result = self.control_plane.submit_job_result(
                job_id,
                device_id=job["device_id"],
                status=status,
                summary=summary,
                artifacts=artifacts or [],
                details={},
                run_id=f"run-{job_id}",
            )
            return JobResultEnvelope(**result)
        return self.complete_job(job_id, summary=summary, artifacts=artifacts, status=status)

    def create_fleet_campaign(
        self, *, name: str, device_ids: list[str], benchmark_scope: list[str]
    ) -> ComparisonCampaign:
        if self.control_plane.enabled:
            return ComparisonCampaign(**self.control_plane.create_campaign(name=name, device_ids=device_ids, benchmark_scope=benchmark_scope))
        return self.create_campaign(name=name, device_ids=device_ids, benchmark_scope=benchmark_scope)

    def list_fleet_devices(self) -> list[FleetDeviceRow]:
        return self.fleet_snapshot().devices

    def list_fleet_jobs(self) -> list[FleetJobRow]:
        if self.control_plane.enabled:
            return self.fleet_snapshot().jobs
        return [
            FleetJobRow(
                job=job,
                status=self._job_status(job.id),
                claimed_at=self._job_claimed_at(job.id),
                completed_at=self._job_completed_at(job.id),
                summary=self._job_summary(job.id),
                artifacts=self._job_artifacts(job.id),
            )
            for job in self._fleet_job_requests()
        ]

    def list_fleet_results(self) -> list[JobResultEnvelope]:
        if self.control_plane.enabled:
            return self.fleet_snapshot().results
        return self._fleet_result_rows()

    def list_fleet_campaigns(self) -> list[ComparisonCampaign]:
        if self.control_plane.enabled:
            return self.fleet_snapshot().campaigns
        return self._fleet_campaign_rows()

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

    def create_demo_run(self, profile_id: str | None = None) -> RunRecord:
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
                    actual="Captured through deterministic demo run.",
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
                notes="Deterministic demo run completed and saved for UI verification.",
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
