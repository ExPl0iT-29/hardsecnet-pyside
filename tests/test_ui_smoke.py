from __future__ import annotations

from pathlib import Path

import pytest

from hardsecnet_pyside.app import HardSecNetController, build_window


def test_main_window_smoke(qapp, tmp_path: Path) -> None:
    pytest.importorskip("PySide6")

    controller = HardSecNetController(project_root=tmp_path / "hardsecnet-pyside")
    window = build_window(controller)

    assert window.nav.count() == 7
    assert window.stack.count() == 7
    window.refresh_all()
    assert "reports" in window.statusBar().currentMessage().lower()
