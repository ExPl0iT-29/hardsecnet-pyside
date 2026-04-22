from __future__ import annotations

from pathlib import Path

import pytest

from hardsecnet_pyside.app import HardSecNetController, build_window


def test_main_window_smoke(qapp, tmp_path: Path) -> None:
    qtwidgets = pytest.importorskip("PySide6.QtWidgets")

    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)

    assert window.nav.count() == 7
    assert window.stack.count() == 7
    assert window.nav.item(0).text() == "Dashboard"
    assert "Benchmark controls" in window.pages["Dashboard"].cards["controls"].label.text()
    button_texts = {button.text() for button in window.findChildren(qtwidgets.QPushButton)}
    assert "Run Local Baseline" in button_texts
    assert "Run Demo" not in button_texts
    window.refresh_all()
    assert "reports" in window.statusBar().currentMessage().lower()
