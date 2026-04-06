from __future__ import annotations

from PySide6 import QtWidgets

from hardsecnet_pyside.ui.pages import (
    AiAdvisorPage,
    BenchmarksPage,
    FleetDashboardPage,
    HardeningPage,
    NetworkPage,
    ReportsPage,
    SettingsPage,
)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.pages: dict[str, QtWidgets.QWidget] = {}
        self._build_ui()
        self.refresh_all()

    def _build_ui(self) -> None:
        root = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(root)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        self.nav = QtWidgets.QListWidget()
        self.nav.setObjectName("Navigation")
        self.nav.setFixedWidth(220)
        self.nav.addItems(
            ["Fleet", "Hardening", "Network", "AI Advisor", "Reports", "Benchmarks", "Settings"]
        )
        self.nav.currentRowChanged.connect(self._select_page)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = {
            "Fleet": FleetDashboardPage(self.controller, self.refresh_all),
            "Hardening": HardeningPage(self.controller, self.refresh_all),
            "Network": NetworkPage(self.controller, self.refresh_all),
            "AI Advisor": AiAdvisorPage(self.controller, self.refresh_all),
            "Reports": ReportsPage(self.controller, self.refresh_all),
            "Benchmarks": BenchmarksPage(self.controller, self.refresh_all),
            "Settings": SettingsPage(self.controller, self.refresh_all),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        side = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("HardSecNet")
        title.setObjectName("AppTitle")
        subtitle = QtWidgets.QLabel("Benchmark-aware hardening studio")
        subtitle.setObjectName("AppSubtitle")
        side.addWidget(title)
        side.addWidget(subtitle)
        side.addWidget(self.nav, 1)

        refresh_button = QtWidgets.QPushButton("Refresh All")
        refresh_button.clicked.connect(self.refresh_all)
        demo_button = QtWidgets.QPushButton("Run Demo")
        demo_button.clicked.connect(self._run_demo)
        side.addWidget(refresh_button)
        side.addWidget(demo_button)

        layout.addLayout(side)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Ready")
        self._apply_style()

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow { background: #0b1220; color: #e5eef8; }
            QLabel#AppTitle { font-size: 24px; font-weight: 700; color: #7ee787; }
            QLabel#AppSubtitle { color: #9fb3c8; margin-bottom: 8px; }
            QLabel#PageTitle { font-size: 22px; font-weight: 700; color: #d9e6ff; }
            QLabel#PageSubtitle { color: #97a6ba; }
            QListWidget#Navigation {
                background: #111827;
                border: 1px solid #243044;
                border-radius: 14px;
                padding: 6px;
                color: #d9e6ff;
            }
            QListWidget#Navigation::item {
                padding: 10px 12px;
                margin: 4px;
                border-radius: 10px;
            }
            QListWidget#Navigation::item:selected { background: #1f6feb; color: white; }
            QGroupBox {
                border: 1px solid #243044;
                border-radius: 12px;
                margin-top: 14px;
                padding: 12px;
                color: #d9e6ff;
            }
            QTableWidget, QTextEdit, QLineEdit, QComboBox {
                background: #0f172a;
                border: 1px solid #243044;
                border-radius: 10px;
                color: #e5eef8;
                padding: 6px;
            }
            QPushButton {
                background: #1f6feb;
                border: none;
                color: white;
                padding: 10px 14px;
                border-radius: 10px;
                font-weight: 600;
            }
            QPushButton:hover { background: #2b7fff; }
            QPushButton:disabled { background: #334155; color: #7b8aa3; }
            """
        )

    def _select_page(self, index: int) -> None:
        if index < 0:
            return
        self.stack.setCurrentIndex(index)
        page = list(self.pages.values())[index]
        refresh = getattr(page, "refresh", None)
        if callable(refresh):
            refresh()

    def refresh_all(self) -> None:
        for page in self.pages.values():
            refresh = getattr(page, "refresh", None)
            if callable(refresh):
                refresh()
        self.nav.setCurrentRow(max(self.nav.currentRow(), 0))
        snapshot = self.controller.get_dashboard_snapshot()
        device = snapshot.device
        self.statusBar().showMessage(
            f"{device.name} | {len(snapshot.reports)} reports | {len(snapshot.runs)} runs | {snapshot.ai_tasks_count} AI tasks"
        )

    def _run_demo(self) -> None:
        hardening = self.pages["Hardening"]
        profile_id = hardening.profile_combo.currentData() if hasattr(hardening, "profile_combo") else None
        if profile_id:
            self.controller.run_profile(profile_id)
            self.refresh_all()
