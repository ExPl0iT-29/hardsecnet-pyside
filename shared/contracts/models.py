from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


Role = Literal["platform_admin", "security_admin", "operator", "viewer", "agent"]
JobStatus = Literal["pending", "approved", "in_progress", "completed", "failed", "cancelled"]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class AccessTokenResponse(ContractModel):
    access_token: str
    token_type: str = "bearer"
    role: Role
    subject: str


class UserBootstrapRequest(ContractModel):
    username: str
    password: str
    display_name: str = ""


class LoginRequest(ContractModel):
    username: str
    password: str


class UserModel(ContractModel):
    id: str
    username: str
    display_name: str = ""
    role: Role
    is_active: bool = True
    created_at: datetime = Field(default_factory=utc_now)


class DeviceEnrollmentTokenRequest(ContractModel):
    device_id: str
    note: str = ""
    expires_in_hours: int = 24


class DeviceEnrollmentRequest(ContractModel):
    enrollment_token: str
    device_id: str
    name: str
    hostname: str
    os_family: Literal["windows", "linux"]
    agent_version: str
    capabilities: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DeviceModel(ContractModel):
    id: str
    name: str
    hostname: str
    os_family: Literal["windows", "linux"]
    agent_mode: str = "fleet"
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
    last_seen: datetime = Field(default_factory=utc_now)


class AgentManifestModel(ContractModel):
    device_id: str
    agent_version: str
    capabilities: list[str] = Field(default_factory=list)
    last_sync: datetime = Field(default_factory=utc_now)


class AgentHeartbeatModel(ContractModel):
    id: str
    device_id: str
    status: str
    queued_jobs: int = 0
    observed_at: datetime = Field(default_factory=utc_now)
    details: dict[str, Any] = Field(default_factory=dict)


class JobCreateRequest(ContractModel):
    device_id: str
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    approval_required: bool = True


class JobModel(ContractModel):
    id: str
    device_id: str
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: JobStatus = "pending"
    approval_required: bool = True
    approval_state: str = "review_required"
    assigned_to: str = ""
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    claimed_at: datetime | None = None
    completed_at: datetime | None = None
    result_summary: str = ""
    artifact_paths: list[str] = Field(default_factory=list)
    error: str = ""


class JobClaimResponse(ContractModel):
    job: JobModel


class JobResultRequest(ContractModel):
    device_id: str
    status: JobStatus
    summary: str
    artifacts: list[str] = Field(default_factory=list)
    details: dict[str, Any] = Field(default_factory=dict)
    run_id: str = ""


class JobResultModel(ContractModel):
    id: str
    job_id: str
    device_id: str
    status: JobStatus
    summary: str
    artifacts: list[str] = Field(default_factory=list)
    reported_at: datetime = Field(default_factory=utc_now)
    details: dict[str, Any] = Field(default_factory=dict)
    run_id: str = ""


class CampaignCreateRequest(ContractModel):
    name: str
    device_ids: list[str]
    benchmark_scope: list[str]


class CampaignModel(ContractModel):
    id: str
    name: str
    device_ids: list[str]
    benchmark_scope: list[str]
    created_at: datetime = Field(default_factory=utc_now)


class ReportIndexModel(ContractModel):
    id: str
    run_id: str = ""
    device_id: str
    job_id: str = ""
    title: str
    generated_at: datetime = Field(default_factory=utc_now)
    json_path: str = ""
    html_path: str = ""
    pdf_path: str = ""
    summary: str = ""


class BenchmarkVersionModel(ContractModel):
    id: str
    os_family: str
    name: str
    version: str
    published_at: datetime = Field(default_factory=utc_now)


class ProfileVersionModel(ContractModel):
    id: str
    os_family: str
    name: str
    version: str
    benchmark_version_id: str = ""
    published_at: datetime = Field(default_factory=utc_now)


class DeviceStatusModel(ContractModel):
    device: DeviceModel
    manifest: AgentManifestModel | None = None
    heartbeat: AgentHeartbeatModel | None = None
    pending_jobs: int = 0
    in_progress_jobs: int = 0
    completed_jobs: int = 0


class FleetSummaryModel(ContractModel):
    devices: list[DeviceStatusModel] = Field(default_factory=list)
    jobs: list[JobModel] = Field(default_factory=list)
    campaigns: list[CampaignModel] = Field(default_factory=list)
    reports: list[ReportIndexModel] = Field(default_factory=list)
    active_device_count: int = 0
    queued_job_count: int = 0
    in_progress_job_count: int = 0
    completed_job_count: int = 0
