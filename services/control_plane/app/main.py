from __future__ import annotations

from contextlib import asynccontextmanager
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from shared.contracts import (
    AccessTokenResponse,
    AgentHeartbeatModel,
    AgentManifestModel,
    BenchmarkVersionModel,
    CampaignCreateRequest,
    CampaignModel,
    DeviceEnrollmentRequest,
    DeviceEnrollmentTokenRequest,
    DeviceModel,
    DeviceStatusModel,
    FleetSummaryModel,
    JobClaimResponse,
    JobCreateRequest,
    JobModel,
    JobResultModel,
    JobResultRequest,
    LoginRequest,
    ProfileVersionModel,
    ReportIndexModel,
    UserBootstrapRequest,
)

from .config import settings
from .database import get_session, init_db
from .db_models import (
    AgentManifest,
    AuditLog,
    BenchmarkVersion,
    Campaign,
    Device,
    EnrollmentToken,
    Heartbeat,
    Job,
    JobResult,
    ProfileVersion,
    ReportIndex,
    User,
)
from .security import create_access_token, decode_token, hash_password, verify_password

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


def _json_loads(value: str, fallback):
    try:
        return json.loads(value)
    except Exception:
        return fallback


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _audit(session: Session, actor: str, action: str, target_type: str, target_id: str, details: dict | None = None) -> None:
    session.add(
        AuditLog(
            actor=actor,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details_json=json.dumps(details or {}, sort_keys=True),
        )
    )
    session.commit()


def _device_model(device: Device) -> DeviceModel:
    return DeviceModel(
        id=device.id,
        name=device.name,
        hostname=device.hostname,
        os_family=device.os_family,  # type: ignore[arg-type]
        agent_mode=device.agent_mode,
        tags=_json_loads(device.tags_json, []),
        metadata=_json_loads(device.metadata_json, {}),
        created_at=device.created_at,
        last_seen=device.last_seen,
    )


def _manifest_model(manifest: AgentManifest) -> AgentManifestModel:
    return AgentManifestModel(
        device_id=manifest.device_id,
        agent_version=manifest.agent_version,
        capabilities=_json_loads(manifest.capabilities_json, []),
        last_sync=manifest.last_sync,
    )


def _heartbeat_model(heartbeat: Heartbeat) -> AgentHeartbeatModel:
    return AgentHeartbeatModel(
        id=heartbeat.id,
        device_id=heartbeat.device_id,
        status=heartbeat.status,
        queued_jobs=heartbeat.queued_jobs,
        observed_at=heartbeat.observed_at,
        details=_json_loads(heartbeat.details_json, {}),
    )


def _job_model(job: Job) -> JobModel:
    return JobModel(
        id=job.id,
        device_id=job.device_id,
        action=job.action,
        payload=_json_loads(job.payload_json, {}),
        status=job.status,  # type: ignore[arg-type]
        approval_required=job.approval_required,
        approval_state=job.approval_state,
        assigned_to=job.assigned_to,
        created_at=job.created_at,
        updated_at=job.updated_at,
        claimed_at=job.claimed_at,
        completed_at=job.completed_at,
        result_summary=job.result_summary,
        artifact_paths=_json_loads(job.artifact_paths_json, []),
        error=job.error,
    )


def _job_result_model(result: JobResult) -> JobResultModel:
    return JobResultModel(
        id=result.id,
        job_id=result.job_id,
        device_id=result.device_id,
        status=result.status,  # type: ignore[arg-type]
        summary=result.summary,
        artifacts=_json_loads(result.artifacts_json, []),
        details=_json_loads(result.details_json, {}),
        run_id=result.run_id,
        reported_at=result.reported_at,
    )


def _campaign_model(campaign: Campaign) -> CampaignModel:
    return CampaignModel(
        id=campaign.id,
        name=campaign.name,
        device_ids=_json_loads(campaign.device_ids_json, []),
        benchmark_scope=_json_loads(campaign.benchmark_scope_json, []),
        created_at=campaign.created_at,
    )


def _report_model(report: ReportIndex) -> ReportIndexModel:
    return ReportIndexModel(
        id=report.id,
        run_id=report.run_id,
        device_id=report.device_id,
        job_id=report.job_id,
        title=report.title,
        generated_at=report.generated_at,
        json_path=report.json_path,
        html_path=report.html_path,
        pdf_path=report.pdf_path,
        summary=report.summary,
    )


def get_current_actor(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> dict:
    try:
        payload = decode_token(token)
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    subject = str(payload.get("sub", ""))
    role = str(payload.get("role", "viewer"))
    if role != "agent":
        user = session.exec(select(User).where(User.username == subject)).first()
        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found")
    return {"sub": subject, "role": role}


def require_roles(*roles: str):
    def dependency(actor: Annotated[dict, Depends(get_current_actor)]) -> dict:
        if actor["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return actor
    return dependency


def _build_fleet_summary(session: Session) -> FleetSummaryModel:
    devices = session.exec(select(Device)).all()
    manifests = {row.device_id: row for row in session.exec(select(AgentManifest)).all()}
    heartbeats = session.exec(select(Heartbeat)).all()
    latest_hb: dict[str, Heartbeat] = {}
    for hb in sorted(heartbeats, key=lambda item: item.observed_at, reverse=True):
        latest_hb.setdefault(hb.device_id, hb)
    jobs = session.exec(select(Job)).all()
    reports = session.exec(select(ReportIndex)).all()
    campaigns = session.exec(select(Campaign)).all()
    device_rows = []
    for device in devices:
        device_jobs = [job for job in jobs if job.device_id == device.id]
        device_rows.append(
            DeviceStatusModel(
                device=_device_model(device),
                manifest=_manifest_model(manifests[device.id]) if device.id in manifests else None,
                heartbeat=_heartbeat_model(latest_hb[device.id]) if device.id in latest_hb else None,
                pending_jobs=sum(1 for job in device_jobs if job.status in {"pending", "approved"}),
                in_progress_jobs=sum(1 for job in device_jobs if job.status == "in_progress"),
                completed_jobs=sum(1 for job in device_jobs if job.status == "completed"),
            )
        )
    return FleetSummaryModel(
        devices=device_rows,
        jobs=[_job_model(item) for item in jobs],
        campaigns=[_campaign_model(item) for item in campaigns],
        reports=[_report_model(item) for item in reports],
        active_device_count=len(device_rows),
        queued_job_count=sum(1 for job in jobs if job.status in {"pending", "approved"}),
        in_progress_job_count=sum(1 for job in jobs if job.status == "in_progress"),
        completed_job_count=sum(1 for job in jobs if job.status == "completed"),
    )


@app.post(f"{settings.api_prefix}/bootstrap/admin", response_model=AccessTokenResponse)
def bootstrap_admin(payload: UserBootstrapRequest, session: Annotated[Session, Depends(get_session)]):
    if session.exec(select(User)).first() is not None:
        raise HTTPException(status_code=400, detail="Admin bootstrap already completed")
    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name or payload.username,
        role="platform_admin",
    )
    session.add(user)
    session.commit()
    _audit(session, payload.username, "bootstrap_admin", "user", payload.username)
    return AccessTokenResponse(
        access_token=create_access_token(payload.username, "platform_admin"),
        role="platform_admin",
        subject=payload.username,
    )


@app.post(f"{settings.api_prefix}/auth/login", response_model=AccessTokenResponse)
def login(payload: LoginRequest, session: Annotated[Session, Depends(get_session)]):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return AccessTokenResponse(
        access_token=create_access_token(user.username, user.role),
        role=user.role,  # type: ignore[arg-type]
        subject=user.username,
    )


@app.post(f"{settings.api_prefix}/devices/enroll-token")
def issue_enrollment_token(
    payload: DeviceEnrollmentTokenRequest,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin"))],
):
    token = secrets.token_urlsafe(24)
    row = EnrollmentToken(
        token=token,
        device_id=payload.device_id,
        note=payload.note,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=payload.expires_in_hours),
        created_by=actor["sub"],
    )
    session.add(row)
    session.commit()
    _audit(session, actor["sub"], "issue_enrollment_token", "device", payload.device_id)
    return {"enrollment_token": token, "device_id": payload.device_id, "expires_at": row.expires_at.isoformat()}


@app.post(f"{settings.api_prefix}/devices/enroll")
def enroll_device(payload: DeviceEnrollmentRequest, session: Annotated[Session, Depends(get_session)]):
    token_row = session.exec(select(EnrollmentToken).where(EnrollmentToken.token == payload.enrollment_token)).first()
    if token_row is None or _as_utc(token_row.expires_at) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired enrollment token")
    if token_row.device_id != payload.device_id:
        raise HTTPException(status_code=400, detail="Enrollment token does not match device id")
    device = session.get(Device, payload.device_id) or Device(
        id=payload.device_id,
        name=payload.name,
        hostname=payload.hostname,
        os_family=payload.os_family,
    )
    device.name = payload.name
    device.hostname = payload.hostname
    device.os_family = payload.os_family
    device.metadata_json = json.dumps(payload.metadata, sort_keys=True)
    device.last_seen = datetime.now(timezone.utc)
    session.add(device)
    manifest = AgentManifest(
        device_id=payload.device_id,
        agent_version=payload.agent_version,
        capabilities_json=json.dumps(payload.capabilities, sort_keys=True),
        last_sync=datetime.now(timezone.utc),
    )
    session.merge(manifest)
    token_row.consumed_at = datetime.now(timezone.utc)
    session.add(token_row)
    session.commit()
    _audit(session, payload.device_id, "device_enroll", "device", payload.device_id)
    return {
        "device": _device_model(device).model_dump(mode="json"),
        "manifest": _manifest_model(manifest).model_dump(mode="json"),
        "access_token": create_access_token(payload.device_id, "agent"),
    }


@app.post(f"{settings.api_prefix}/devices/{{device_id}}/heartbeat", response_model=AgentHeartbeatModel)
def record_heartbeat(
    device_id: str,
    payload: AgentHeartbeatModel,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "agent"))],
):
    device = session.get(Device, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    if actor["role"] == "agent" and actor["sub"] != device_id:
        raise HTTPException(status_code=403, detail="Agent token does not match device")
    heartbeat = Heartbeat(
        id=payload.id,
        device_id=device_id,
        status=payload.status,
        queued_jobs=payload.queued_jobs,
        observed_at=payload.observed_at,
        details_json=json.dumps(payload.details, sort_keys=True),
    )
    device.last_seen = payload.observed_at
    session.add(heartbeat)
    session.add(device)
    session.commit()
    _audit(session, actor["sub"], "record_heartbeat", "device", device_id)
    return _heartbeat_model(heartbeat)


@app.get(f"{settings.api_prefix}/devices", response_model=list[DeviceStatusModel])
def list_devices(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    return _build_fleet_summary(session).devices


@app.get(f"{settings.api_prefix}/devices/{{device_id}}", response_model=DeviceStatusModel)
def get_device(
    device_id: str,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    for row in _build_fleet_summary(session).devices:
        if row.device.id == device_id:
            return row
    raise HTTPException(status_code=404, detail="Device not found")


@app.post(f"{settings.api_prefix}/jobs", response_model=JobModel)
def create_job(
    payload: JobCreateRequest,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator"))],
):
    if session.get(Device, payload.device_id) is None:
        raise HTTPException(status_code=404, detail="Device not found")
    initial = "pending" if payload.approval_required else "approved"
    job = Job(
        id=f"job-{uuid.uuid4().hex[:12]}",
        device_id=payload.device_id,
        action=payload.action,
        payload_json=json.dumps(payload.payload, sort_keys=True),
        approval_required=payload.approval_required,
        approval_state=initial,
        status=initial,
    )
    session.add(job)
    session.commit()
    _audit(session, actor["sub"], "create_job", "job", job.id)
    return _job_model(job)


@app.get(f"{settings.api_prefix}/jobs", response_model=list[JobModel])
def list_jobs(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer", "agent"))],
    device_id: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
):
    query = select(Job)
    if device_id:
        query = query.where(Job.device_id == device_id)
    if status_filter:
        query = query.where(Job.status == status_filter)
    jobs = session.exec(query).all()
    if actor["role"] == "agent":
        jobs = [job for job in jobs if job.device_id == actor["sub"]]
    return [_job_model(item) for item in jobs]


@app.post(f"{settings.api_prefix}/jobs/{{job_id}}/approve", response_model=JobModel)
def approve_job(
    job_id: str,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin"))],
):
    job = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = "approved"
    job.approval_state = "approved"
    job.updated_at = datetime.now(timezone.utc)
    session.add(job)
    session.commit()
    _audit(session, actor["sub"], "approve_job", "job", job_id)
    return _job_model(job)


@app.post(f"{settings.api_prefix}/jobs/{{job_id}}/claim", response_model=JobClaimResponse)
def claim_job(
    job_id: str,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "agent"))],
):
    job = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if actor["role"] == "agent" and actor["sub"] != job.device_id:
        raise HTTPException(status_code=403, detail="Agent token does not match device")
    if job.status not in {"approved", "pending"}:
        raise HTTPException(status_code=409, detail="Job is not claimable")
    job.status = "in_progress"
    job.claimed_at = datetime.now(timezone.utc)
    job.updated_at = job.claimed_at
    job.assigned_to = actor["sub"]
    session.add(job)
    session.commit()
    _audit(session, actor["sub"], "claim_job", "job", job_id)
    return JobClaimResponse(job=_job_model(job))


@app.post(f"{settings.api_prefix}/jobs/{{job_id}}/result", response_model=JobResultModel)
def submit_job_result(
    job_id: str,
    payload: JobResultRequest,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "agent"))],
):
    job = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.device_id != payload.device_id:
        raise HTTPException(status_code=400, detail="Job/device mismatch")
    if actor["role"] == "agent" and actor["sub"] != payload.device_id:
        raise HTTPException(status_code=403, detail="Agent token does not match device")
    job.status = payload.status
    job.completed_at = datetime.now(timezone.utc)
    job.updated_at = job.completed_at
    job.result_summary = payload.summary
    job.artifact_paths_json = json.dumps(payload.artifacts, sort_keys=True)
    job.error = payload.details.get("error", "")
    session.add(job)
    result = JobResult(
        id=f"jobresult-{uuid.uuid4().hex[:12]}",
        job_id=job_id,
        device_id=payload.device_id,
        status=payload.status,
        summary=payload.summary,
        artifacts_json=json.dumps(payload.artifacts, sort_keys=True),
        details_json=json.dumps(payload.details, sort_keys=True),
        run_id=payload.run_id,
    )
    session.add(result)
    artifact_dir = settings.artifacts_dir / payload.device_id / job_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    report = ReportIndex(
        id=f"report-{uuid.uuid4().hex[:12]}",
        run_id=payload.run_id,
        device_id=payload.device_id,
        job_id=job_id,
        title=f"{job.action} report for {payload.device_id}",
        json_path=str(artifact_dir / "result.json"),
        html_path=str(artifact_dir / "result.html"),
        pdf_path=str(artifact_dir / "result.pdf"),
        summary=payload.summary,
    )
    Path(report.json_path).write_text(json.dumps(payload.model_dump(mode="json"), indent=2), encoding="utf-8")
    Path(report.html_path).write_text(f"<html><body><h1>{report.title}</h1><p>{payload.summary}</p></body></html>", encoding="utf-8")
    Path(report.pdf_path).write_text(payload.summary, encoding="utf-8")
    session.add(report)
    session.commit()
    _audit(session, actor["sub"], "submit_job_result", "job", job_id)
    return _job_result_model(result)


@app.get(f"{settings.api_prefix}/fleet/summary", response_model=FleetSummaryModel)
def fleet_summary(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    return _build_fleet_summary(session)


@app.get(f"{settings.api_prefix}/campaigns", response_model=list[CampaignModel])
def list_campaigns(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    return [_campaign_model(item) for item in session.exec(select(Campaign)).all()]


@app.post(f"{settings.api_prefix}/campaigns", response_model=CampaignModel)
def create_campaign(
    payload: CampaignCreateRequest,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator"))],
):
    row = Campaign(
        id=f"campaign-{uuid.uuid4().hex[:12]}",
        name=payload.name,
        device_ids_json=json.dumps(payload.device_ids, sort_keys=True),
        benchmark_scope_json=json.dumps(payload.benchmark_scope, sort_keys=True),
    )
    session.add(row)
    session.commit()
    _audit(session, actor["sub"], "create_campaign", "campaign", row.id)
    return _campaign_model(row)


@app.get(f"{settings.api_prefix}/reports", response_model=list[ReportIndexModel])
def list_reports(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    return [_report_model(item) for item in session.exec(select(ReportIndex)).all()]


@app.get(f"{settings.api_prefix}/reports/{{report_id}}", response_model=ReportIndexModel)
def get_report(
    report_id: str,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    row = session.get(ReportIndex, report_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return _report_model(row)


@app.get(f"{settings.api_prefix}/benchmark-versions", response_model=list[BenchmarkVersionModel])
def list_benchmark_versions(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    rows = session.exec(select(BenchmarkVersion)).all()
    return [BenchmarkVersionModel(id=r.id, os_family=r.os_family, name=r.name, version=r.version, published_at=r.published_at) for r in rows]


@app.post(f"{settings.api_prefix}/benchmark-versions", response_model=BenchmarkVersionModel)
def publish_benchmark_version(
    payload: BenchmarkVersionModel,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin"))],
):
    row = BenchmarkVersion(**payload.model_dump())
    session.merge(row)
    session.commit()
    _audit(session, actor["sub"], "publish_benchmark_version", "benchmark_version", row.id)
    return payload


@app.get(f"{settings.api_prefix}/profile-versions", response_model=list[ProfileVersionModel])
def list_profile_versions(
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin", "operator", "viewer"))],
):
    rows = session.exec(select(ProfileVersion)).all()
    return [ProfileVersionModel(id=r.id, os_family=r.os_family, name=r.name, version=r.version, benchmark_version_id=r.benchmark_version_id, published_at=r.published_at) for r in rows]


@app.post(f"{settings.api_prefix}/profile-versions", response_model=ProfileVersionModel)
def publish_profile_version(
    payload: ProfileVersionModel,
    session: Annotated[Session, Depends(get_session)],
    actor: Annotated[dict, Depends(require_roles("platform_admin", "security_admin"))],
):
    row = ProfileVersion(**payload.model_dump())
    session.merge(row)
    session.commit()
    _audit(session, actor["sub"], "publish_profile_version", "profile_version", row.id)
    return payload
