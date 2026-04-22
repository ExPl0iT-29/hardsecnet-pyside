from __future__ import annotations

import json
import platform
import sqlite3
import uuid
from dataclasses import asdict
from importlib import resources
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar

from hardsecnet_pyside.config import AppPaths
from hardsecnet_pyside.models import (
    AITaskRecord,
    AgentHeartbeat,
    AgentManifest,
    ApprovalRecord,
    BenchmarkDocument,
    BenchmarkItem,
    CheckLogic,
    ComparisonCampaign,
    ComparisonDelta,
    ComplianceFinding,
    DeviceRecord,
    EvidenceField,
    JobRequest,
    JobResultEnvelope,
    ModuleResult,
    ProfileTemplate,
    RemediationStep,
    ReportBundle,
    RunRecord,
    StepResult,
)

T = TypeVar("T")


TABLE_DEFINITIONS = {
    "devices": """
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            os_family TEXT NOT NULL,
            hostname TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "benchmark_documents": """
        CREATE TABLE IF NOT EXISTS benchmark_documents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            os_family TEXT NOT NULL,
            source_type TEXT NOT NULL,
            imported_at TEXT NOT NULL,
            status TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "benchmark_items": """
        CREATE TABLE IF NOT EXISTS benchmark_items (
            id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            benchmark_id TEXT NOT NULL,
            title TEXT NOT NULL,
            os_family TEXT NOT NULL,
            status TEXT NOT NULL,
            confidence REAL NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "profiles": """
        CREATE TABLE IF NOT EXISTS profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            os_family TEXT NOT NULL,
            strictness TEXT NOT NULL,
            built_in INTEGER NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "runs": """
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            profile_id TEXT NOT NULL,
            os_family TEXT NOT NULL,
            status TEXT NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            payload TEXT NOT NULL
        )
    """,
    "findings": """
        CREATE TABLE IF NOT EXISTS findings (
            id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            benchmark_id TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "comparisons": """
        CREATE TABLE IF NOT EXISTS comparisons (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            before_run_id TEXT NOT NULL,
            after_run_id TEXT NOT NULL,
            benchmark_id TEXT NOT NULL,
            delta_type TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "reports": """
        CREATE TABLE IF NOT EXISTS reports (
            id TEXT PRIMARY KEY,
            run_id TEXT NOT NULL,
            comparison_id TEXT NOT NULL,
            title TEXT NOT NULL,
            generated_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "approvals": """
        CREATE TABLE IF NOT EXISTS approvals (
            id TEXT PRIMARY KEY,
            target_type TEXT NOT NULL,
            target_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            decided_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "ai_tasks": """
        CREATE TABLE IF NOT EXISTS ai_tasks (
            id TEXT PRIMARY KEY,
            agent_type TEXT NOT NULL,
            subject_type TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            provider TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            payload TEXT NOT NULL
        )
    """,
    "agent_manifests": """
        CREATE TABLE IF NOT EXISTS agent_manifests (
            device_id TEXT PRIMARY KEY,
            payload TEXT NOT NULL
        )
    """,
    "agent_heartbeats": """
        CREATE TABLE IF NOT EXISTS agent_heartbeats (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            status TEXT NOT NULL,
            queued_jobs INTEGER NOT NULL,
            observed_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "jobs": """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            device_id TEXT NOT NULL,
            action TEXT NOT NULL,
            status TEXT NOT NULL,
            approval_state TEXT NOT NULL,
            created_at TEXT NOT NULL,
            completed_at TEXT,
            payload TEXT NOT NULL
        )
    """,
    "job_results": """
        CREATE TABLE IF NOT EXISTS job_results (
            id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            device_id TEXT NOT NULL,
            status TEXT NOT NULL,
            reported_at TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "comparison_campaigns": """
        CREATE TABLE IF NOT EXISTS comparison_campaigns (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """,
    "settings": """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """,
}


def _deserialize_benchmark_item(data: dict[str, Any]) -> BenchmarkItem:
    data.setdefault("script_path", "")
    data.setdefault("script_state", "unmapped")
    data.setdefault("review_notes", [])
    return BenchmarkItem(
        **{key: value for key, value in data.items() if key not in {"audit_logic", "remediation_steps", "evidence_fields"}},
        audit_logic=[CheckLogic(**entry) for entry in data.get("audit_logic", [])],
        remediation_steps=[RemediationStep(**entry) for entry in data.get("remediation_steps", [])],
        evidence_fields=[EvidenceField(**entry) for entry in data.get("evidence_fields", [])],
    )


def _deserialize_run(data: dict[str, Any]) -> RunRecord:
    return RunRecord(
        **{key: value for key, value in data.items() if key not in {"module_results"}},
        module_results=[
            ModuleResult(
                **{key: value for key, value in item.items() if key not in {"steps"}},
                steps=[StepResult(**step) for step in item.get("steps", [])],
            )
            for item in data.get("module_results", [])
        ],
    )


DESERIALIZERS: dict[type[Any], Callable[[dict[str, Any]], Any]] = {
    BenchmarkDocument: lambda data: BenchmarkDocument(**data),
    BenchmarkItem: _deserialize_benchmark_item,
    ProfileTemplate: lambda data: ProfileTemplate(**data),
    DeviceRecord: lambda data: DeviceRecord(**data),
    RunRecord: _deserialize_run,
    ComplianceFinding: lambda data: ComplianceFinding(**data),
    ComparisonDelta: lambda data: ComparisonDelta(**data),
    ReportBundle: lambda data: ReportBundle(**data),
    ApprovalRecord: lambda data: ApprovalRecord(**data),
    AITaskRecord: lambda data: AITaskRecord(**data),
    AgentManifest: lambda data: AgentManifest(**data),
    AgentHeartbeat: lambda data: AgentHeartbeat(**data),
    JobRequest: lambda data: JobRequest(**data),
    JobResultEnvelope: lambda data: JobResultEnvelope(**data),
    ComparisonCampaign: lambda data: ComparisonCampaign(**data),
}


class HardSecNetRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            for ddl in TABLE_DEFINITIONS.values():
                conn.execute(ddl)
            conn.commit()

    def _upsert(self, table: str, record_id: str, columns: dict[str, Any], payload: dict[str, Any]) -> None:
        keys = ["id", *columns.keys(), "payload"]
        values = [record_id, *columns.values(), json.dumps(payload, indent=2, sort_keys=True)]
        placeholders = ", ".join("?" for _ in keys)
        updates = ", ".join(f"{key}=excluded.{key}" for key in keys[1:])
        with self.connect() as conn:
            conn.execute(
                f"""
                INSERT INTO {table} ({", ".join(keys)})
                VALUES ({placeholders})
                ON CONFLICT(id) DO UPDATE SET
                {updates}
                """,
                values,
            )
            conn.commit()

    def _list(self, table: str, cls: type[T], where: str = "", params: Iterable[Any] = ()) -> list[T]:
        query = f"SELECT payload FROM {table}"
        if where:
            query += f" WHERE {where}"
        with self.connect() as conn:
            rows = conn.execute(query, tuple(params)).fetchall()
        parser = DESERIALIZERS[cls]
        return [parser(json.loads(row["payload"])) for row in rows]

    def _get(self, table: str, cls: type[T], record_id: str) -> T | None:
        with self.connect() as conn:
            row = conn.execute(f"SELECT payload FROM {table} WHERE id = ?", (record_id,)).fetchone()
        if row is None:
            return None
        parser = DESERIALIZERS[cls]
        return parser(json.loads(row["payload"]))

    def set_setting(self, key: str, value: str) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )
            conn.commit()

    def get_setting(self, key: str, default: str = "") -> str:
        with self.connect() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return default if row is None else str(row["value"])

    def save_device(self, device: DeviceRecord) -> None:
        self._upsert(
            "devices",
            device.id,
            {
                "name": device.name,
                "os_family": device.os_family,
                "hostname": device.hostname,
                "last_seen": device.last_seen,
            },
            asdict(device),
        )

    def list_devices(self) -> list[DeviceRecord]:
        return self._list("devices", DeviceRecord)

    def get_device(self, device_id: str) -> DeviceRecord | None:
        return self._get("devices", DeviceRecord, device_id)

    def save_benchmark_document(self, document: BenchmarkDocument) -> None:
        self._upsert(
            "benchmark_documents",
            document.id,
            {
                "name": document.name,
                "version": document.version,
                "os_family": document.os_family,
                "source_type": document.source_type,
                "imported_at": document.imported_at,
                "status": document.status,
            },
            asdict(document),
        )

    def list_benchmark_documents(self) -> list[BenchmarkDocument]:
        return self._list("benchmark_documents", BenchmarkDocument)

    def get_benchmark_document(self, document_id: str) -> BenchmarkDocument | None:
        return self._get("benchmark_documents", BenchmarkDocument, document_id)

    def save_benchmark_items(self, items: list[BenchmarkItem]) -> None:
        for item in items:
            self._upsert(
                "benchmark_items",
                item.id,
                {
                    "document_id": item.document_id,
                    "benchmark_id": item.benchmark_id,
                    "title": item.title,
                    "os_family": item.os_family,
                    "status": item.status,
                    "confidence": item.confidence,
                },
                asdict(item),
            )

    def list_benchmark_items(
        self, document_id: str | None = None, os_family: str | None = None
    ) -> list[BenchmarkItem]:
        clauses: list[str] = []
        params: list[Any] = []
        if document_id:
            clauses.append("document_id = ?")
            params.append(document_id)
        if os_family:
            clauses.append("os_family = ?")
            params.append(os_family)
        return self._list("benchmark_items", BenchmarkItem, " AND ".join(clauses), params)

    def save_profile(self, profile: ProfileTemplate) -> None:
        self._upsert(
            "profiles",
            profile.id,
            {
                "name": profile.name,
                "os_family": profile.os_family,
                "strictness": profile.strictness,
                "built_in": int(profile.built_in),
            },
            asdict(profile),
        )

    def list_profiles(self, os_family: str | None = None) -> list[ProfileTemplate]:
        if os_family:
            return self._list("profiles", ProfileTemplate, "os_family = ?", (os_family,))
        return self._list("profiles", ProfileTemplate)

    def get_profile(self, profile_id: str) -> ProfileTemplate | None:
        return self._get("profiles", ProfileTemplate, profile_id)

    def save_run(self, run: RunRecord) -> None:
        self._upsert(
            "runs",
            run.id,
            {
                "device_id": run.device_id,
                "profile_id": run.profile_id,
                "os_family": run.os_family,
                "status": run.status,
                "started_at": run.started_at,
                "ended_at": run.ended_at,
            },
            asdict(run),
        )

    def list_runs(self, device_id: str | None = None) -> list[RunRecord]:
        if device_id:
            return self._list("runs", RunRecord, "device_id = ?", (device_id,))
        return self._list("runs", RunRecord)

    def get_run(self, run_id: str) -> RunRecord | None:
        return self._get("runs", RunRecord, run_id)

    def save_findings(self, findings: list[ComplianceFinding]) -> None:
        for finding in findings:
            self._upsert(
                "findings",
                finding.id,
                {
                    "run_id": finding.run_id,
                    "benchmark_id": finding.benchmark_id,
                    "title": finding.title,
                    "status": finding.status,
                    "severity": finding.severity,
                    "confidence": finding.confidence,
                },
                asdict(finding),
            )

    def list_findings(self, run_id: str | None = None) -> list[ComplianceFinding]:
        if run_id:
            return self._list("findings", ComplianceFinding, "run_id = ?", (run_id,))
        return self._list("findings", ComplianceFinding)

    def save_comparisons(self, comparisons: list[ComparisonDelta]) -> None:
        for comparison in comparisons:
            self._upsert(
                "comparisons",
                comparison.id,
                {
                    "device_id": comparison.device_id,
                    "before_run_id": comparison.before_run_id,
                    "after_run_id": comparison.after_run_id,
                    "benchmark_id": comparison.benchmark_id,
                    "delta_type": comparison.delta_type,
                },
                asdict(comparison),
            )

    def list_comparisons(
        self, after_run_id: str | None = None, device_id: str | None = None
    ) -> list[ComparisonDelta]:
        clauses: list[str] = []
        params: list[Any] = []
        if after_run_id:
            clauses.append("after_run_id = ?")
            params.append(after_run_id)
        if device_id:
            clauses.append("device_id = ?")
            params.append(device_id)
        return self._list("comparisons", ComparisonDelta, " AND ".join(clauses), params)

    def save_report(self, report: ReportBundle) -> None:
        self._upsert(
            "reports",
            report.id,
            {
                "run_id": report.run_id,
                "comparison_id": report.comparison_id,
                "title": report.title,
                "generated_at": report.generated_at,
            },
            asdict(report),
        )

    def list_reports(self) -> list[ReportBundle]:
        return self._list("reports", ReportBundle)

    def get_report(self, report_id: str) -> ReportBundle | None:
        return self._get("reports", ReportBundle, report_id)

    def save_approval(self, approval: ApprovalRecord) -> None:
        self._upsert(
            "approvals",
            approval.id,
            {
                "target_type": approval.target_type,
                "target_id": approval.target_id,
                "decision": approval.decision,
                "reviewer": approval.reviewer,
                "decided_at": approval.decided_at,
            },
            asdict(approval),
        )

    def list_approvals(self) -> list[ApprovalRecord]:
        return self._list("approvals", ApprovalRecord)

    def save_ai_task(self, task: AITaskRecord) -> None:
        self._upsert(
            "ai_tasks",
            task.id,
            {
                "agent_type": task.agent_type,
                "subject_type": task.subject_type,
                "subject_id": task.subject_id,
                "provider": task.provider,
                "status": task.status,
                "created_at": task.created_at,
                "completed_at": task.completed_at,
            },
            asdict(task),
        )

    def list_ai_tasks(self, subject_id: str | None = None) -> list[AITaskRecord]:
        if subject_id:
            return self._list("ai_tasks", AITaskRecord, "subject_id = ?", (subject_id,))
        return self._list("ai_tasks", AITaskRecord)

    def save_agent_manifest(self, manifest: AgentManifest) -> None:
        payload = json.dumps(asdict(manifest), indent=2, sort_keys=True)
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO agent_manifests (device_id, payload)
                VALUES (?, ?)
                ON CONFLICT(device_id) DO UPDATE SET payload = excluded.payload
                """,
                (manifest.device_id, payload),
            )
            conn.commit()

    def list_agent_manifests(self) -> list[AgentManifest]:
        return self._list("agent_manifests", AgentManifest)

    def get_agent_manifest(self, device_id: str) -> AgentManifest | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT payload FROM agent_manifests WHERE device_id = ?", (device_id,)
            ).fetchone()
        if row is None:
            return None
        return AgentManifest(**json.loads(row["payload"]))

    def save_agent_heartbeat(self, heartbeat: AgentHeartbeat) -> None:
        self._upsert(
            "agent_heartbeats",
            heartbeat.id,
            {
                "device_id": heartbeat.device_id,
                "status": heartbeat.status,
                "queued_jobs": heartbeat.queued_jobs,
                "observed_at": heartbeat.observed_at,
            },
            asdict(heartbeat),
        )

    def list_agent_heartbeats(self, device_id: str | None = None) -> list[AgentHeartbeat]:
        if device_id:
            return self._list("agent_heartbeats", AgentHeartbeat, "device_id = ?", (device_id,))
        return self._list("agent_heartbeats", AgentHeartbeat)

    def latest_agent_heartbeat(self, device_id: str) -> AgentHeartbeat | None:
        heartbeats = sorted(
            self.list_agent_heartbeats(device_id=device_id),
            key=lambda item: (item.observed_at, item.id),
            reverse=True,
        )
        return heartbeats[0] if heartbeats else None

    def save_job(self, job: JobRequest) -> None:
        self._upsert(
            "jobs",
            job.id,
            {
                "device_id": job.device_id,
                "action": job.action,
                "status": job.status,
                "approval_state": job.approval_state,
                "created_at": job.created_at,
                "completed_at": job.completed_at,
            },
            asdict(job),
        )

    def list_jobs(
        self,
        device_id: str | None = None,
        status: str | None = None,
    ) -> list[JobRequest]:
        clauses: list[str] = []
        params: list[Any] = []
        if device_id:
            clauses.append("device_id = ?")
            params.append(device_id)
        if status:
            clauses.append("status = ?")
            params.append(status)
        return self._list("jobs", JobRequest, " AND ".join(clauses), params)

    def get_job(self, job_id: str) -> JobRequest | None:
        return self._get("jobs", JobRequest, job_id)

    def save_job_result(self, result: JobResultEnvelope) -> None:
        result_id = result.id or f"jobresult-{uuid.uuid4().hex[:12]}"
        result.id = result_id
        self._upsert(
            "job_results",
            result.id,
            {
                "job_id": result.job_id,
                "device_id": result.device_id,
                "status": result.status,
                "reported_at": result.reported_at,
            },
            asdict(result),
        )

    def list_job_results(
        self,
        device_id: str | None = None,
        job_id: str | None = None,
    ) -> list[JobResultEnvelope]:
        clauses: list[str] = []
        params: list[Any] = []
        if device_id:
            clauses.append("device_id = ?")
            params.append(device_id)
        if job_id:
            clauses.append("job_id = ?")
            params.append(job_id)
        return self._list("job_results", JobResultEnvelope, " AND ".join(clauses), params)

    def save_campaign(self, campaign: ComparisonCampaign) -> None:
        self._upsert("comparison_campaigns", campaign.id, {"name": campaign.name}, asdict(campaign))

    def list_campaigns(self) -> list[ComparisonCampaign]:
        return self._list("comparison_campaigns", ComparisonCampaign)

    def bootstrap(self, paths: AppPaths) -> None:
        current_device_id = self.get_setting("current_device_id") or f"device-{uuid.uuid4().hex[:12]}"
        self.set_setting("current_device_id", current_device_id)
        current_device = DeviceRecord(
            id=current_device_id,
            name="Local Device",
            os_family="windows" if platform.system().lower().startswith("win") else "linux",
            hostname=platform.node() or "localhost",
            metadata={"managed_by": "hardsecnet-pyside"},
        )
        self.save_device(current_device)
        self.save_agent_manifest(
            AgentManifest(
                device_id=current_device.id,
                agent_version="0.1.0",
                capabilities=["local-audit", "local-hardening", "reporting", "benchmark-import"],
            )
        )

        if not self.list_profiles():
            raw_profiles = json.loads(
                resources.files("hardsecnet_pyside.resources")
                .joinpath("default_profiles.json")
                .read_text(encoding="utf-8")
            )
            for item in raw_profiles["profiles"]:
                self.save_profile(ProfileTemplate(**item))

        if not self.list_benchmark_documents():
            raw_benchmarks = json.loads(
                resources.files("hardsecnet_pyside.resources")
                .joinpath("default_benchmarks.json")
                .read_text(encoding="utf-8")
            )
            for document in raw_benchmarks["documents"]:
                self.save_benchmark_document(BenchmarkDocument(**document))
            items = []
            for item in raw_benchmarks["items"]:
                items.append(
                    BenchmarkItem(
                        **{
                            key: value
                            for key, value in item.items()
                            if key not in {"audit_logic", "remediation_steps", "evidence_fields"}
                        },
                        audit_logic=[CheckLogic(**entry) for entry in item["audit_logic"]],
                        remediation_steps=[RemediationStep(**entry) for entry in item["remediation_steps"]],
                        evidence_fields=[EvidenceField(**entry) for entry in item["evidence_fields"]],
                    )
                )
            self.save_benchmark_items(items)
