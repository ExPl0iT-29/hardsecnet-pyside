from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from hardsecnet_pyside.app import HardSecNetController, build_window


def test_main_window_smoke(qapp, tmp_path: Path) -> None:
    qtwidgets = pytest.importorskip("PySide6.QtWidgets")

    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)

    assert window.nav.count() == 6
    assert window.stack.count() == 6
    assert window.nav.item(0).text() == "Dashboard"
    assert {window.nav.item(index).text() for index in range(window.nav.count())} == {
        "Dashboard",
        "Hardening",
        "AI Advisor",
        "Reports",
        "Profile Builder",
        "Settings",
    }
    assert "QMainWindow { background: #eef3f8" in window.styleSheet()
    assert "QPushButton#PrimaryButton" in window.styleSheet()
    assert "Compliance Score" in window.pages["Dashboard"].cards["score"].label.text()
    assert "AI" not in window.pages["Dashboard"].subtitle_label.text()
    button_texts = {button.text() for button in window.findChildren(qtwidgets.QPushButton)}
    assert "Run Local Baseline" in button_texts
    assert "Save Selected As Profile" in button_texts
    assert "Check Ready Settings" in button_texts
    assert "Harden Ready Settings" in button_texts
    assert "Harden Selected Script" in button_texts
    assert "Open HTML" in button_texts
    assert "Open PDF" in button_texts
    assert "Add Device" not in button_texts
    assert "Run Demo" not in button_texts
    window.refresh_all()
    assert "reports" in window.statusBar().currentMessage().lower()
    assert "AI" not in window.statusBar().currentMessage()


def test_hardening_profile_switch_updates_profile_details(qapp, tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)
    hardening = window.pages["Hardening"]

    hardening.refresh()
    assert hardening.profile_combo.count() >= 2

    first_text = hardening.details.toPlainText()
    first_modules = hardening.module_table.rowCount()
    assert "Profile:" in first_text

    hardening.profile_combo.setCurrentIndex(1)
    qapp.processEvents()

    second_text = hardening.details.toPlainText()
    second_modules = hardening.module_table.rowCount()

    assert first_text != second_text
    assert "Profile:" in second_text
    assert first_modules != second_modules or hardening.profile_combo.itemText(0) != hardening.profile_combo.itemText(1)


def test_profile_builder_supports_add_and_remove_selection(qapp, tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)
    builder = window.pages["Profile Builder"]

    builder.refresh()
    assert builder.documents_table.rowCount() >= 1
    assert builder.items_table.rowCount() >= 2

    builder.items_table.selectRow(0)
    builder._add_selected_items()
    qapp.processEvents()

    assert builder.selection_table.rowCount() == 1
    assert "Added 1 control" in builder.details.toPlainText()

    builder.selection_table.selectRow(0)
    builder._remove_selected_items()
    qapp.processEvents()

    assert builder.selection_table.rowCount() == 0
    assert "Removed 1 control" in builder.details.toPlainText()


def test_hardening_execution_output_uses_clearer_labels(qapp, tmp_path: Path) -> None:
    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)
    hardening = window.pages["Hardening"]

    lines = hardening._format_script_executions(
        [
            SimpleNamespace(
                benchmark_id="17.7.4",
                id="script-admin",
                mode="status",
                status="blocked",
                output="",
                error="This script requires an elevated Administrator session. Relaunch the app from an elevated terminal to check or apply this control.",
                artifact_path="artifact-admin.json",
            ),
            SimpleNamespace(
                benchmark_id="9.3.1",
                id="script-firewall",
                mode="status",
                status="completed",
                output="Setting: Example\nStatus: OFF",
                error="",
                artifact_path="artifact-firewall.json",
            ),
        ]
    )

    rendered = "\n".join(lines)
    assert "Admin Required" in rendered
    assert "Run the app from an Administrator terminal" in rendered
    assert "Status: Not Hardened Yet" in rendered
