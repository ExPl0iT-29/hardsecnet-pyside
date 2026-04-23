from __future__ import annotations

from pathlib import Path

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
