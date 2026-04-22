from __future__ import annotations

from pathlib import Path

from hardsecnet_pyside.app import HardSecNetController


def test_bootstrap_and_snapshot(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    snapshot = controller.get_dashboard_snapshot()

    assert snapshot.device.id
    assert snapshot.profiles
    assert snapshot.reports == []
    assert snapshot.module_catalog


def test_run_profile_creates_report_and_tasks(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    device = controller.get_current_device()
    profile = controller.list_profiles(device.os_family)[0]

    result = controller.run_profile(profile.id)

    assert result.run.id.startswith("run-")
    assert result.report.json_path
    assert Path(result.report.json_path).exists()
    assert Path(result.report.html_path).exists()
    assert Path(result.report.pdf_path).exists()
    assert controller.list_reports()
    assert controller.list_ai_tasks(result.run.id)

    payload = controller.export_report_payload(result.report.id)
    assert payload["report"]["id"] == result.report.id
    assert payload["run"]["id"] == result.run.id
    assert payload["device"]["id"] == device.id
    assert payload["findings"]


def test_import_benchmark_creates_profile_and_document(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    import_path = tmp_path / "sample_benchmark.txt"
    import_path.write_text(
        "\n".join(
            [
                "1.1.1 Disable unused services",
                "1.1.2 Enforce stronger logon policy",
                "1.4.1 Configure firewall baseline",
            ]
        ),
        encoding="utf-8",
    )

    before_documents = len(controller.list_benchmark_documents())
    before_profiles = len(controller.list_profiles())

    document = controller.import_benchmark(import_path)

    assert Path(document.source_path).name == import_path.name
    assert Path(document.source_path).parent == controller.paths.imports_dir
    assert Path(document.source_path).exists()
    assert len(controller.list_benchmark_documents()) == before_documents + 1
    assert len(controller.list_profiles()) >= before_profiles + 1
    assert controller.list_ai_tasks(document.id)


def test_script_readiness_and_dry_run_record_artifact(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    import_path = tmp_path / "cis_ubuntu_sample.txt"
    import_path.write_text(
        "\n".join(
            [
                "3.2.1 Ensure dccp kernel module is not available",
                "Remediation:",
                "Run modprobe -r dccp to unload the module after approval.",
            ]
        ),
        encoding="utf-8",
    )

    document = controller.import_benchmark(import_path)
    items = controller.list_benchmark_items(document.id)
    readiness = controller.list_script_readiness(document.id)

    assert items
    assert readiness
    assert readiness[0].item_id == items[0].id
    assert Path(readiness[0].script_path).exists()
    assert readiness[0].status == "review_required"

    execution = controller.run_script_dry_run(readiness[0].item_id, operator="pytest")

    assert execution.status == "dry_run_recorded"
    assert execution.mode == "dry_run"
    assert execution.operator == "pytest"
    assert execution.readiness_status == "review_required"
    assert Path(execution.artifact_path).exists()
    assert controller.list_script_executions(readiness[0].item_id)[0].id == execution.id


def test_bootstrap_adds_curated_ready_scripts(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")

    readiness = controller.list_script_readiness(document_id="builtin-doc-windows")
    ready = [item for item in readiness if item.status == "ready"]

    assert ready
    assert ready[0].script_path
    assert Path(ready[0].script_path).exists()
    assert ready[0].commands_preview
