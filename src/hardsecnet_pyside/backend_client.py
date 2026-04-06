from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from hardsecnet_pyside.config import ControlPlaneSettings


@dataclass(slots=True)
class ControlPlaneClient:
    settings: ControlPlaneSettings
    token: str = ""

    @property
    def enabled(self) -> bool:
        return bool(self.settings.base_url)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def connect(self) -> None:
        if not self.enabled:
            return
        bootstrap = httpx.post(
            f"{self.settings.base_url}/api/v1/bootstrap/admin",
            json={"username": self.settings.username, "password": self.settings.password},
            timeout=20.0,
        )
        if bootstrap.status_code not in {200, 400}:
            bootstrap.raise_for_status()
        login = httpx.post(
            f"{self.settings.base_url}/api/v1/auth/login",
            json={"username": self.settings.username, "password": self.settings.password},
            timeout=20.0,
        )
        login.raise_for_status()
        self.token = login.json()["access_token"]

    def fleet_summary(self) -> dict[str, Any]:
        self.connect()
        response = httpx.get(
            f"{self.settings.base_url}/api/v1/fleet/summary",
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def issue_enrollment_token(self, device_id: str) -> str:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/devices/enroll-token",
            json={"device_id": device_id},
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()["enrollment_token"]

    def enroll_device(self, *, device_id: str, name: str, hostname: str, os_family: str, agent_version: str, capabilities: list[str], metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        token = self.issue_enrollment_token(device_id)
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/devices/enroll",
            json={
                "enrollment_token": token,
                "device_id": device_id,
                "name": name,
                "hostname": hostname,
                "os_family": os_family,
                "agent_version": agent_version,
                "capabilities": capabilities,
                "metadata": metadata or {},
            },
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def create_job(self, *, device_id: str, action: str, payload: dict[str, Any], approval_required: bool = True) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/jobs",
            json={
                "device_id": device_id,
                "action": action,
                "payload": payload,
                "approval_required": approval_required,
            },
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def approve_job(self, job_id: str) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/jobs/{job_id}/approve",
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def create_campaign(self, *, name: str, device_ids: list[str], benchmark_scope: list[str]) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/campaigns",
            json={"name": name, "device_ids": device_ids, "benchmark_scope": benchmark_scope},
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def record_heartbeat(
        self,
        *,
        device_id: str,
        status: str,
        queued_jobs: int,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/devices/{device_id}/heartbeat",
            json={
                "id": f"heartbeat-{device_id}",
                "device_id": device_id,
                "status": status,
                "queued_jobs": queued_jobs,
                "details": details or {},
            },
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def list_jobs(
        self,
        *,
        device_id: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        self.connect()
        params: dict[str, Any] = {}
        if device_id:
            params["device_id"] = device_id
        if status:
            params["status"] = status
        response = httpx.get(
            f"{self.settings.base_url}/api/v1/jobs",
            params=params,
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def claim_job(self, job_id: str) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/jobs/{job_id}/claim",
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()["job"]

    def submit_job_result(
        self,
        job_id: str,
        *,
        device_id: str,
        status: str,
        summary: str,
        artifacts: list[str] | None = None,
        details: dict[str, Any] | None = None,
        run_id: str = "",
    ) -> dict[str, Any]:
        self.connect()
        response = httpx.post(
            f"{self.settings.base_url}/api/v1/jobs/{job_id}/result",
            json={
                "device_id": device_id,
                "status": status,
                "summary": summary,
                "artifacts": artifacts or [],
                "details": details or {},
                "run_id": run_id,
            },
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()

    def list_reports(self) -> list[dict[str, Any]]:
        self.connect()
        response = httpx.get(
            f"{self.settings.base_url}/api/v1/reports",
            headers=self._headers(),
            timeout=20.0,
        )
        response.raise_for_status()
        return response.json()
