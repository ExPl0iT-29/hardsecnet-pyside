from __future__ import annotations

from pathlib import Path

import pytest

from hardsecnet_pyside.app import HardSecNetController, build_window


def test_fleet_control_plane_flow(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")

    manifest = controller.enroll_fleet_device(
        device_id="fleet-01",
        name="Fleet Device 01",
        os_family="linux",
        hostname="fleet-01.local",
        capabilities=["audit", "compare"],
    )
    heartbeat = controller.record_fleet_heartbeat("fleet-01", "healthy", 0)
    job = controller.queue_fleet_job(
        "fleet-01",
        "remote-audit",
        {"benchmark_scope": ["CIS Linux"], "run_mode": "audit"},
    )
    claimed = controller.claim_fleet_job(job.id)
    result = controller.complete_fleet_job(
        job.id,
        summary="Remote audit completed successfully.",
        artifacts=["artifact-01.json"],
    )
    campaign = controller.create_fleet_campaign(
        name="Linux Baseline Campaign",
        device_ids=["fleet-01"],
        benchmark_scope=["CIS Linux"],
    )

    snapshot = controller.fleet_snapshot()
    fleet_device = next(row for row in snapshot.devices if row.device.id == "fleet-01")

    assert manifest.device_id == "fleet-01"
    assert heartbeat.status == "healthy"
    assert claimed.id == job.id
    assert result.job_id == job.id
    assert result.artifacts == ["artifact-01.json"]
    assert campaign.name == "Linux Baseline Campaign"
    assert fleet_device.heartbeat_status == "completed"
    assert fleet_device.queued_jobs == 0
    assert any(item.job.id == job.id and item.status == "completed" for item in snapshot.jobs)
    assert any(item.job_id == job.id for item in snapshot.results)
    assert any(item.id == campaign.id for item in snapshot.campaigns)


def test_fleet_control_plane_rejects_unknown_targets(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")

    with pytest.raises(ValueError):
        controller.record_fleet_heartbeat("missing", "healthy", 0)

    with pytest.raises(ValueError):
        controller.claim_fleet_job("missing-job")

    with pytest.raises(ValueError):
        controller.complete_fleet_job("missing-job", summary="done")


def test_fleet_snapshot_includes_current_device(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    snapshot = controller.fleet_snapshot()

    assert snapshot.active_device_count >= 1
    assert any(row.device.id == controller.get_current_device().id for row in snapshot.devices)
