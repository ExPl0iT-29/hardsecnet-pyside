from __future__ import annotations

import json
import uuid
from pathlib import Path

from shared.contracts import AgentHeartbeatModel, DeviceEnrollmentRequest, JobResultRequest

from .adapters.linux import LinuxAdapter
from .adapters.windows import WindowsAdapter
from .client import ControlPlaneClient
from .config import AgentConfig


class DeviceAgent:
    def __init__(self, config: AgentConfig | None = None) -> None:
        self.config = config or AgentConfig()
        self.config.ensure()
        self.client = ControlPlaneClient(self.config.control_plane_url)
        self.adapter = WindowsAdapter(self.config.workspace_root) if self.config.os_family == "windows" else LinuxAdapter(self.config.workspace_root)
        self.state_file = self.config.state_dir / "agent-state.json"

    def ensure_enrolled(self) -> None:
        if self.client.token:
            return
        self.client.bootstrap_admin(self.config.username, self.config.password)
        self.client.login(self.config.username, self.config.password)
        token = self.config.enrollment_token or self.client.issue_enrollment_token(self.config.device_id)
        payload = DeviceEnrollmentRequest(
            enrollment_token=token,
            device_id=self.config.device_id,
            name=self.config.device_name,
            hostname=self.config.hostname,
            os_family=self.config.os_family,  # type: ignore[arg-type]
            agent_version="0.1.0",
            capabilities=["remote-audit", "remote-harden", "remote-compare"],
            metadata={"managed_by": "hardsecnet-device-agent"},
        )
        self.client.enroll(payload)

    def poll_once(self) -> None:
        self.ensure_enrolled()
        queued_jobs = self.client.list_jobs(self.config.device_id, status="approved")
        self.client.heartbeat(
            self.config.device_id,
            AgentHeartbeatModel(
                id=f"heartbeat-{uuid.uuid4().hex[:12]}",
                device_id=self.config.device_id,
                status="healthy",
                queued_jobs=len(queued_jobs),
            ),
        )
        if not queued_jobs:
            return
        job = self.client.claim_job(queued_jobs[0]["id"])
        result = self.adapter.execute(job["action"], job.get("payload", {}))
        artifact_file = self.config.state_dir / f"{job['id']}.json"
        artifact_file.write_text(json.dumps(result.details, indent=2), encoding="utf-8")
        self.client.submit_result(
            job["id"],
            JobResultRequest(
                device_id=self.config.device_id,
                status=result.status,  # type: ignore[arg-type]
                summary=result.summary,
                artifacts=[str(artifact_file)],
                details=result.details,
            ),
        )


if __name__ == "__main__":
    DeviceAgent().poll_once()
