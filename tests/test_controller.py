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
    expected_items = [
        item
        for item in controller.list_benchmark_items(os_family=device.os_family)
        if item.benchmark_id in set(profile.benchmark_ids)
    ] or controller.list_benchmark_items(os_family=device.os_family)

    result = controller.run_profile(profile.id)

    assert result.run.id.startswith("run-")
    assert len(result.findings) == len(expected_items)
    assert result.run.summary["benchmark_scope"] == "profile_selected_controls"
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
    assert len(payload["findings"]) == len(expected_items)
    html = Path(result.report.html_path).read_text(encoding="utf-8")
    assert all(item.benchmark_id in html for item in expected_items)


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


def test_add_device_and_switch_current_device(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    original = controller.get_current_device()

    added = controller.add_local_device(
        name="Ubuntu Demo",
        os_family="linux",
        hostname="ubuntu-demo",
    )

    assert added.id != original.id
    assert controller.get_current_device().id == added.id
    assert added in controller.list_devices()

    controller.set_current_device(original.id)
    assert controller.get_current_device().id == original.id


def test_harden_execution_is_gated_and_uses_apply_flag(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    ready = [item for item in controller.list_script_readiness(os_family="windows") if item.status == "ready"]

    execution = controller.run_script_dry_run(ready[0].item_id, execute=True, operator="pytest")

    assert execution.status == "blocked"
    assert "-Apply" in execution.command
    assert "HARDSECNET_ALLOW_SCRIPT_EXECUTION=1" in execution.error


def test_windows_cis_benchmark_profiles_cover_imported_controls(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    windows_items = controller.list_benchmark_items(os_family="windows")
    full_profile = controller.repository.get_profile("cis_windows_11_full_benchmark")
    firewall_profile = controller.repository.get_profile("cis_windows_11_firewall")

    assert len(windows_items) >= 2
    assert full_profile is not None
    assert len(full_profile.benchmark_ids) == len(windows_items)
    if firewall_profile is not None:
        assert all(item.startswith("9.") for item in firewall_profile.benchmark_ids)


def test_deharden_execution_is_gated_and_uses_rollback_flag(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    ready = [item for item in controller.list_script_readiness(os_family="windows") if item.status == "ready"]

    execution = controller.rollback_script(ready[0].item_id, operator="pytest")

    assert execution.status == "blocked"
    assert execution.mode == "rollback"
    assert "-Rollback" in execution.command
    assert execution.operator == "pytest"
    assert "HARDSECNET_ALLOW_SCRIPT_EXECUTION=1" in execution.error


def test_ready_script_status_check_runs_without_live_execution_gate(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    ready = [item for item in controller.list_script_readiness(os_family="windows") if item.status == "ready"]

    execution = controller.check_script_status(ready[0].item_id, operator="pytest")

    assert execution.mode == "status"
    assert "-Status" in execution.command
    assert execution.status in {"completed", "failed"}
    assert "HARDSECNET_ALLOW_SCRIPT_EXECUTION=1" not in execution.error


def test_admin_required_status_check_is_blocked_cleanly_when_not_elevated(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    readiness = next(
        (item for item in controller.list_script_readiness(os_family="windows") if item.benchmark_id == "17.7.4"),
        None,
    )
    if readiness is None:
        return

    execution = controller.check_script_status(readiness.item_id, operator="pytest")

    assert execution.mode == "status"
    assert execution.status == "blocked"
    assert "requires an elevated Administrator session" in execution.error


def test_windows_workstation_profile_has_broad_scope_and_multiple_ready_settings(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    profile = controller.repository.get_profile("demo_windows_workstation_hardening")
    ready = controller.list_script_readiness(os_family="windows")

    assert profile is not None
    profile_ready = [item for item in ready if item.status == "ready" and item.benchmark_id in profile.benchmark_ids]
    assert len(profile_ready) >= 6
    assert {item.benchmark_id for item in profile_ready} >= {
        "CIS-Windows-11-1.4.1",
        "CIS-Windows-Demo-FileExtensions",
        "CIS-Windows-Demo-Autorun",
        "CIS-Windows-Demo-ZoneInformation",
        "CIS-Windows-Demo-ScreenSaverActive",
        "CIS-Windows-Demo-ScreenSaverTimeout",
    }
    assert "CIS-Windows-Workstation-PasswordPolicy" in profile.benchmark_ids
    assert "CIS-Windows-Workstation-FirewallPolicy" in profile.benchmark_ids
    if any(item.benchmark_id.startswith("1.") for item in controller.list_benchmark_items(os_family="windows")):
        assert any(benchmark_id.startswith("1.") for benchmark_id in profile.benchmark_ids)
    if any(item.benchmark_id.startswith("9.") for item in controller.list_benchmark_items(os_family="windows")):
        assert any(benchmark_id.startswith("9.") for benchmark_id in profile.benchmark_ids)


def test_demo_profile_list_hides_legacy_windows_clutter(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    names = [profile.name for profile in controller.list_profiles("windows")]
    ids = [profile.id for profile in controller.list_profiles("windows")]

    assert "CIS Windows 11 Full Benchmark" in names
    assert "Windows Workstation Hardening" in names
    assert "Windows Removable Media Safety" in names
    assert "Password Expiry And Public Firewall" in names
    assert "Private And Public Firewall On" in names
    if any(item.benchmark_id.startswith("9.") for item in controller.list_benchmark_items(os_family="windows")):
        assert "CIS Windows 11 Firewall" in names
    assert "Default Windows Desktop" not in names
    assert "Strict Candidate" not in names
    assert not any(profile_id.startswith("profile-doc-") for profile_id in ids)


def test_password_expiry_and_public_firewall_profile_has_expected_scope(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    profile = controller.repository.get_profile("demo_windows_password_expiry_public_firewall")

    assert profile is not None
    assert "1.1.2" in profile.benchmark_ids
    assert set(profile.benchmark_ids).issuperset(
        {"9.3.1", "9.3.2", "9.3.3", "9.3.4", "9.3.5", "9.3.6", "9.3.7", "9.3.8", "9.3.9", "17.7.4"}
    )


def test_private_and_public_firewall_on_profile_has_expected_scope(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    profile = controller.repository.get_profile("demo_windows_private_public_firewall_on")

    assert profile is not None
    assert profile.benchmark_ids == ["9.2.1", "9.3.1"]


def test_demo_profile_list_hides_legacy_linux_clutter(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    names = [profile.name for profile in controller.list_profiles("linux")]
    ids = [profile.id for profile in controller.list_profiles("linux")]

    assert "CIS Ubuntu 24.04 Full Benchmark" in names
    assert "Default Ubuntu Desktop" not in names
    assert not any(profile_id.startswith("profile-doc-") for profile_id in ids)


def test_ubuntu_profile_scopes_to_selected_controls(tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    controller.add_local_device(name="Ubuntu Test", os_family="linux", hostname="ubuntu-test")
    profile = controller.repository.get_profile("cis_ubuntu_2404_full_benchmark")

    assert profile is not None
    result = controller.run_profile(profile.id, operator="pytest")

    assert result.run.summary["benchmark_scope"] == "profile_selected_controls"
    assert result.run.summary["benchmark_count"] == len(result.findings)
    assert {finding.benchmark_id for finding in result.findings}.issuperset(set(profile.benchmark_ids))
