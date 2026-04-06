from __future__ import annotations

from pathlib import Path

from hardsecnet_pyside.app import HardSecNetController


class FakeControlPlane:
    enabled = True

    def __init__(self) -> None:
        self.jobs = [
            {
                "id": "job-remote-01",
                "device_id": "fleet-01",
                "action": "remote-audit",
                "payload": {"module": "Networking"},
                "status": "approved",
                "approval_required": False,
                "approval_state": "approved",
                "assigned_to": "",
                "created_at": "2026-04-04T00:00:00+00:00",
                "updated_at": "2026-04-04T00:00:00+00:00",
                "claimed_at": None,
                "completed_at": None,
                "result_summary": "",
                "artifact_paths": [],
                "error": "",
            }
        ]
        self.reports = []

    def fleet_summary(self):
        return {
            "devices": [
                {
                    "device": {
                        "id": "fleet-01",
                        "name": "Fleet 01",
                        "hostname": "fleet-01.local",
                        "os_family": "linux",
                        "agent_mode": "fleet",
                        "tags": [],
                        "metadata": {},
                        "last_seen": "2026-04-04T00:00:00+00:00",
                    },
                    "manifest": {
                        "device_id": "fleet-01",
                        "agent_version": "0.1.0",
                        "capabilities": ["remote-audit"],
                        "last_sync": "2026-04-04T00:00:00+00:00",
                    },
                    "heartbeat": {
                        "id": "heartbeat-fleet-01",
                        "device_id": "fleet-01",
                        "status": "healthy",
                        "queued_jobs": 1,
                        "observed_at": "2026-04-04T00:00:00+00:00",
                        "details": {},
                    },
                    "pending_jobs": 1,
                }
            ],
            "jobs": self.jobs,
            "campaigns": [
                {
                    "id": "campaign-01",
                    "name": "Linux Baseline",
                    "device_ids": ["fleet-01"],
                    "benchmark_scope": ["CIS Linux"],
                    "created_at": "2026-04-04T00:00:00+00:00",
                }
            ],
            "reports": self.reports,
            "active_device_count": 1,
            "queued_job_count": sum(1 for job in self.jobs if job["status"] in {"pending", "approved"}),
            "completed_job_count": sum(1 for job in self.jobs if job["status"] == "completed"),
        }

    def record_heartbeat(self, *, device_id: str, status: str, queued_jobs: int):
        return {
            "id": f"heartbeat-{device_id}",
            "device_id": device_id,
            "status": status,
            "queued_jobs": queued_jobs,
            "observed_at": "2026-04-04T00:00:00+00:00",
            "details": {},
        }

    def claim_job(self, job_id: str):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = "in_progress"
                job["claimed_at"] = "2026-04-04T00:01:00+00:00"
                job["updated_at"] = "2026-04-04T00:01:00+00:00"
                return job
        raise ValueError(job_id)

    def list_jobs(self):
        return self.jobs

    def submit_job_result(
        self,
        job_id: str,
        *,
        device_id: str,
        status: str,
        summary: str,
        artifacts: list[str] | None = None,
        details: dict | None = None,
        run_id: str = "",
    ):
        for job in self.jobs:
            if job["id"] == job_id:
                job["status"] = status
                job["completed_at"] = "2026-04-04T00:02:00+00:00"
                job["updated_at"] = "2026-04-04T00:02:00+00:00"
                job["result_summary"] = summary
                job["artifact_paths"] = list(artifacts or [])
                result = {
                    "id": "jobresult-01",
                    "job_id": job_id,
                    "device_id": device_id,
                    "status": status,
                    "summary": summary,
                    "artifacts": list(artifacts or []),
                    "details": details or {},
                    "run_id": run_id,
                    "reported_at": "2026-04-04T00:02:00+00:00",
                }
                self.reports = [
                    {
                        "id": "report-01",
                        "run_id": run_id,
                        "device_id": device_id,
                        "job_id": job_id,
                        "title": "Remote audit report",
                        "generated_at": "2026-04-04T00:02:00+00:00",
                        "json_path": "artifact.json",
                        "html_path": "artifact.html",
                        "pdf_path": "artifact.pdf",
                        "summary": summary,
                    }
                ]
                return result
        raise ValueError(job_id)


def test_controller_uses_backend_mode_for_fleet_flow(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    controller.control_plane = FakeControlPlane()

    snapshot = controller.fleet_snapshot()
    heartbeat = controller.record_fleet_heartbeat("fleet-01", "healthy", 1)
    claimed = controller.claim_fleet_job("job-remote-01")
    result = controller.complete_fleet_job(
        "job-remote-01",
        summary="Remote audit complete",
        artifacts=["artifact.json"],
    )
    refreshed = controller.fleet_snapshot()

    assert snapshot.active_device_count == 1
    assert heartbeat.device_id == "fleet-01"
    assert claimed.status == "in_progress"
    assert result.job_id == "job-remote-01"
    assert refreshed.completed_job_count == 1
    assert refreshed.results[0].summary == "Remote audit complete"
