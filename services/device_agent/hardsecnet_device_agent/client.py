from __future__ import annotations

from typing import Any

import httpx

from shared.contracts import AgentHeartbeatModel, DeviceEnrollmentRequest, JobResultRequest


class ControlPlaneClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = ""

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def bootstrap_admin(self, username: str, password: str) -> None:
        response = httpx.post(f"{self.base_url}/api/v1/bootstrap/admin", json={"username": username, "password": password})
        if response.status_code == 400:
            return
        response.raise_for_status()

    def login(self, username: str, password: str) -> None:
        response = httpx.post(
            f"{self.base_url}/api/v1/auth/login",
            json={"username": username, "password": password},
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]

    def issue_enrollment_token(self, device_id: str) -> str:
        response = httpx.post(
            f"{self.base_url}/api/v1/devices/enroll-token",
            json={"device_id": device_id},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()["enrollment_token"]

    def enroll(self, payload: DeviceEnrollmentRequest) -> None:
        response = httpx.post(
            f"{self.base_url}/api/v1/devices/enroll",
            json=payload.model_dump(mode="json"),
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]

    def heartbeat(self, device_id: str, payload: AgentHeartbeatModel) -> None:
        response = httpx.post(
            f"{self.base_url}/api/v1/devices/{device_id}/heartbeat",
            json=payload.model_dump(mode="json"),
            headers=self._headers(),
        )
        response.raise_for_status()

    def list_jobs(self, device_id: str, status: str = "approved") -> list[dict[str, Any]]:
        response = httpx.get(
            f"{self.base_url}/api/v1/jobs",
            params={"device_id": device_id, "status": status},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()

    def claim_job(self, job_id: str) -> dict[str, Any]:
        response = httpx.post(
            f"{self.base_url}/api/v1/jobs/{job_id}/claim",
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()["job"]

    def submit_result(self, job_id: str, payload: JobResultRequest) -> dict[str, Any]:
        response = httpx.post(
            f"{self.base_url}/api/v1/jobs/{job_id}/result",
            json=payload.model_dump(mode="json"),
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json()
