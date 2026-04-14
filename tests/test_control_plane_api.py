from __future__ import annotations

import importlib
import os
from pathlib import Path

from fastapi.testclient import TestClient


def _load_test_app(tmp_path: Path):
    os.environ["HARDSECNET_CP_DATABASE_URL"] = f"sqlite:///{(tmp_path / 'cp.db').as_posix()}"
    os.environ["HARDSECNET_CP_ARTIFACTS_DIR"] = str(tmp_path / "artifacts")
    config = importlib.import_module("services.control_plane.app.config")
    database = importlib.import_module("services.control_plane.app.database")
    main = importlib.import_module("services.control_plane.app.main")
    importlib.reload(config)
    importlib.reload(database)
    reloaded = importlib.reload(main)
    return reloaded.app


def _auth_headers(client: TestClient) -> dict[str, str]:
    bootstrap = client.post("/api/v1/bootstrap/admin", json={"username": "admin", "password": "admin"})
    assert bootstrap.status_code in {200, 400}
    login = client.post("/api/v1/auth/login", json={"username": "admin", "password": "admin"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_control_plane_enrollment_and_job_flow(tmp_path: Path) -> None:
    app = _load_test_app(tmp_path)
    with TestClient(app) as client:
        headers = _auth_headers(client)
        issued = client.post("/api/v1/devices/enroll-token", json={"device_id": "agent-01"}, headers=headers)
        assert issued.status_code == 200
        enrollment_token = issued.json()["enrollment_token"]

        enrolled = client.post(
            "/api/v1/devices/enroll",
            json={
                "enrollment_token": enrollment_token,
                "device_id": "agent-01",
                "name": "Agent 01",
                "hostname": "agent-01.local",
                "os_family": "linux",
                "agent_version": "0.1.0",
                "capabilities": ["remote-audit"],
                "metadata": {},
            },
        )
        assert enrolled.status_code == 200
        agent_token = enrolled.json()["access_token"]

        heartbeat = client.post(
            "/api/v1/devices/agent-01/heartbeat",
            json={
                "id": "hb-01",
                "device_id": "agent-01",
                "status": "healthy",
                "queued_jobs": 0,
                "details": {},
            },
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert heartbeat.status_code == 200

        job = client.post(
            "/api/v1/jobs",
            json={"device_id": "agent-01", "action": "remote-audit", "payload": {"module": "Networking"}, "approval_required": False},
            headers=headers,
        )
        assert job.status_code == 200
        job_id = job.json()["id"]

        claimed = client.post(f"/api/v1/jobs/{job_id}/claim", headers={"Authorization": f"Bearer {agent_token}"})
        assert claimed.status_code == 200
        assert claimed.json()["job"]["status"] == "in_progress"

        result = client.post(
            f"/api/v1/jobs/{job_id}/result",
            json={
                "device_id": "agent-01",
                "status": "completed",
                "summary": "Audit complete",
                "artifacts": ["artifact.json"],
                "details": {},
                "run_id": "run-01",
            },
            headers={"Authorization": f"Bearer {agent_token}"},
        )
        assert result.status_code == 200

        summary = client.get("/api/v1/fleet/summary", headers=headers)
        assert summary.status_code == 200
        payload = summary.json()
        assert payload["active_device_count"] == 1
        assert payload["completed_job_count"] == 1

        reports = client.get("/api/v1/reports", headers=headers)
        assert reports.status_code == 200
        assert len(reports.json()) == 1


def test_control_plane_allows_dashboard_cors(tmp_path: Path) -> None:
    app = _load_test_app(tmp_path)
    with TestClient(app) as client:
        response = client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": "http://127.0.0.1:4173",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:4173"
