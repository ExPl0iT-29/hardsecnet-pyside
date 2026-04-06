from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    display_name: str = ""
    role: str = "platform_admin"
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)


class EnrollmentToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(index=True, unique=True)
    device_id: str = Field(index=True)
    note: str = ""
    expires_at: datetime = Field(default_factory=lambda: utc_now() + timedelta(hours=24))
    created_by: str = ""
    created_at: datetime = Field(default_factory=utc_now)
    consumed_at: datetime | None = None


class Device(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    hostname: str
    os_family: str = Field(index=True)
    agent_mode: str = "fleet"
    tags_json: str = "[]"
    metadata_json: str = "{}"
    created_at: datetime = Field(default_factory=utc_now)
    last_seen: datetime = Field(default_factory=utc_now)


class AgentManifest(SQLModel, table=True):
    device_id: str = Field(primary_key=True, foreign_key="device.id")
    agent_version: str
    capabilities_json: str = "[]"
    last_sync: datetime = Field(default_factory=utc_now)


class Heartbeat(SQLModel, table=True):
    id: str = Field(primary_key=True)
    device_id: str = Field(foreign_key="device.id", index=True)
    status: str
    queued_jobs: int = 0
    observed_at: datetime = Field(default_factory=utc_now)
    details_json: str = "{}"


class Job(SQLModel, table=True):
    id: str = Field(primary_key=True)
    device_id: str = Field(foreign_key="device.id", index=True)
    action: str
    payload_json: str = "{}"
    status: str = Field(index=True, default="pending")
    approval_required: bool = True
    approval_state: str = "review_required"
    assigned_to: str = ""
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    claimed_at: datetime | None = None
    completed_at: datetime | None = None
    result_summary: str = ""
    artifact_paths_json: str = "[]"
    error: str = ""


class JobResult(SQLModel, table=True):
    id: str = Field(primary_key=True)
    job_id: str = Field(foreign_key="job.id", index=True, unique=True)
    device_id: str = Field(foreign_key="device.id", index=True)
    status: str
    summary: str
    artifacts_json: str = "[]"
    details_json: str = "{}"
    run_id: str = ""
    reported_at: datetime = Field(default_factory=utc_now)


class Campaign(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    device_ids_json: str = "[]"
    benchmark_scope_json: str = "[]"
    created_at: datetime = Field(default_factory=utc_now)


class ReportIndex(SQLModel, table=True):
    id: str = Field(primary_key=True)
    run_id: str = ""
    device_id: str = Field(index=True)
    job_id: str = Field(index=True, default="")
    title: str
    generated_at: datetime = Field(default_factory=utc_now)
    json_path: str = ""
    html_path: str = ""
    pdf_path: str = ""
    summary: str = ""


class BenchmarkVersion(SQLModel, table=True):
    id: str = Field(primary_key=True)
    os_family: str
    name: str
    version: str
    published_at: datetime = Field(default_factory=utc_now)


class ProfileVersion(SQLModel, table=True):
    id: str = Field(primary_key=True)
    os_family: str
    name: str
    version: str
    benchmark_version_id: str = ""
    published_at: datetime = Field(default_factory=utc_now)


class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    actor: str
    action: str
    target_type: str
    target_id: str
    details_json: str = "{}"
    created_at: datetime = Field(default_factory=utc_now)
