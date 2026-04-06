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
