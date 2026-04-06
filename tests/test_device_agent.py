from __future__ import annotations

from pathlib import Path

from services.device_agent.hardsecnet_device_agent.adapters.windows import WindowsAdapter
from services.device_agent.hardsecnet_device_agent.main import DeviceAgent


def test_windows_adapter_reports_missing_script(tmp_path: Path) -> None:
    adapter = WindowsAdapter(tmp_path)
    result = adapter.execute("remote-audit", {})
    assert result.status == "failed"
    assert "not found" in result.summary.lower()


def test_device_agent_poll_once_with_fake_client(tmp_path: Path) -> None:
    agent = DeviceAgent()
    agent.config.state_dir = tmp_path
    agent.state_file = tmp_path / "agent-state.json"

    class FakeClient:
        def __init__(self):
            self.token = "token"
            self.claimed = False
            self.result_sent = False

        def list_jobs(self, device_id: str, status: str = "approved"):
            return [{"id": "job-01", "action": "remote-audit", "payload": {"module": "Networking"}}]

        def heartbeat(self, device_id, payload):
            self.heartbeat_payload = payload

        def claim_job(self, job_id: str):
            self.claimed = True
            return {"id": job_id, "action": "remote-audit", "payload": {"module": "Networking"}}

        def submit_result(self, job_id, payload):
            self.result_sent = True
            self.payload = payload
            return {"id": "jobresult-01"}

        def bootstrap_admin(self, username, password):
            return None

        def login(self, username, password):
            self.token = "token"

        def issue_enrollment_token(self, device_id: str) -> str:
            return "token"

        def enroll(self, payload):
            self.token = "agent-token"

    class FakeAdapter:
        def execute(self, action: str, payload: dict):
            return type("Result", (), {"status": "completed", "summary": "ok", "details": {"note": "done"}})()

    agent.client = FakeClient()
    agent.adapter = FakeAdapter()
    agent.poll_once()

    assert agent.client.claimed is True
    assert agent.client.result_sent is True
    assert agent.client.payload.summary == "ok"
