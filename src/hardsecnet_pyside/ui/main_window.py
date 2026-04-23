from __future__ import annotations

import os
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from hardsecnet_pyside.ui.bridge import WebBridge


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        
        # Setup WebEngineView
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.setWindowTitle("HardSecNet - Local CIS Hardening Studio")
        self.setMinimumSize(1180, 760)

        # Setup WebChannel and Bridge
        self.channel = QWebChannel()
        self.bridge = WebBridge(self.controller)
        self.channel.registerObject("backend", self.bridge)
        self.browser.page().setWebChannel(self.channel)

        # Load the local HTML file
        web_dir = Path(__file__).resolve().parent.parent / "web"
        index_path = web_dir / "index.html"
        self.browser.setUrl(QtCore.QUrl.fromLocalFile(str(index_path)))
        
        # Connect bridge signal to force refresh if needed
        self.bridge.snapshotUpdated.connect(self._on_snapshot_updated)

    def _on_snapshot_updated(self, payload: str):
        # The JS frontend already listens to this signal directly, 
        # but we could add desktop-level notifications here if desired.
        pass

    def refresh_all(self) -> None:
        # Called by app.py or externally
        self.bridge.refreshSnapshot()
