from __future__ import annotations

from PySide6 import QtWidgets

from hardsecnet_pyside.ui.pages import (
    AiAdvisorPage,
    BenchmarksPage,
    DashboardPage,
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
        self.setMinimumSize(1180, 760)
        root = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        self.nav = QtWidgets.QListWidget()
        self.nav.setObjectName("Navigation")
        self.nav.setFixedWidth(220)
        self.nav.addItems(
            ["Dashboard", "Hardening", "Network", "AI Advisor", "Reports", "Benchmarks", "Settings"]
        )
        self.nav.currentRowChanged.connect(self._select_page)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = {
            "Dashboard": DashboardPage(self.controller, self.refresh_all),
            "Hardening": HardeningPage(self.controller, self.refresh_all),
            "Network": NetworkPage(self.controller, self.refresh_all),
            "AI Advisor": AiAdvisorPage(self.controller, self.refresh_all),
            "Reports": ReportsPage(self.controller, self.refresh_all),
            "Benchmarks": BenchmarksPage(self.controller, self.refresh_all),
            "Settings": SettingsPage(self.controller, self.refresh_all),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        side_panel = QtWidgets.QFrame()
        side_panel.setObjectName("Sidebar")
        side = QtWidgets.QVBoxLayout(side_panel)
        side.setContentsMargins(14, 14, 14, 14)
        side.setSpacing(10)
        title = QtWidgets.QLabel("HardSecNet")
        title.setObjectName("AppTitle")
        subtitle = QtWidgets.QLabel("Local CIS hardening studio")
        subtitle.setObjectName("AppSubtitle")
        side.addWidget(title)
        side.addWidget(subtitle)
        side.addWidget(self.nav, 1)

        refresh_button = QtWidgets.QPushButton("Refresh All")
        refresh_button.clicked.connect(self.refresh_all)
        baseline_button = QtWidgets.QPushButton("Run Local Baseline")
        baseline_button.clicked.connect(self._run_local_baseline)
        side.addWidget(refresh_button)
        side.addWidget(baseline_button)

        layout.addWidget(side_panel)
        layout.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.statusBar().showMessage("Ready")
        self._apply_style()

    def _apply_style(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow { background: #111318; color: #eef3f7; }
            QWidget { color: #eef3f7; font-size: 13px; }
            QFrame#Sidebar {
                background: #191d24;
                border: 1px solid #2f3742;
                border-radius: 8px;
            }
            QLabel#AppTitle { font-size: 25px; font-weight: 700; color: #7dd3c7; }
            QLabel#AppSubtitle { color: #b7c5cf; margin-bottom: 8px; }
            QLabel#PageTitle { font-size: 24px; font-weight: 700; color: #f4f7fb; }
            QLabel#PageSubtitle { color: #aebac5; margin-bottom: 8px; }
            QLabel#SectionTitle { color: #e8edf2; font-size: 15px; font-weight: 700; }
            QLabel#PanelTitle { color: #f4f7fb; font-size: 16px; font-weight: 700; }
            QLabel#PanelText { color: #b7c5cf; }
            QListWidget#Navigation {
                background: #111318;
                border: 1px solid #2f3742;
                border-radius: 8px;
                padding: 6px;
                color: #dce7ee;
            }
            QListWidget#Navigation::item {
                padding: 10px 12px;
                margin: 4px;
                border-radius: 6px;
            }
            QListWidget#Navigation::item:selected { background: #257c75; color: white; }
            QListWidget#Navigation::item:hover { background: #252b34; }
            QFrame#MetricCard, QFrame#Panel {
                background: #1b2028;
                border: 1px solid #343d49;
                border-radius: 8px;
            }
            QFrame#MetricCard[accent="cyan"] { border-top: 3px solid #39c5d8; }
            QFrame#MetricCard[accent="green"] { border-top: 3px solid #7bc96f; }
            QFrame#MetricCard[accent="amber"] { border-top: 3px solid #e3b341; }
            QFrame#MetricCard[accent="coral"] { border-top: 3px solid #e16f5c; }
            QFrame#MetricCard[accent="violet"] { border-top: 3px solid #a78bfa; }
            QFrame#MetricCard[accent="blue"] { border-top: 3px solid #67a7ff; }
            QLabel#MetricValue { font-size: 28px; font-weight: 700; color: #ffffff; }
            QLabel#MetricLabel { color: #b7c5cf; }
            QGroupBox {
                border: 1px solid #343d49;
                border-radius: 8px;
                margin-top: 14px;
                padding: 12px;
                color: #e8edf2;
                font-weight: 700;
            }
            QTableWidget, QTextEdit, QLineEdit, QComboBox {
                background: #171b22;
                border: 1px solid #343d49;
                border-radius: 8px;
                color: #eef3f7;
                padding: 6px;
            }
            QHeaderView::section {
                background: #252b34;
                color: #dce7ee;
                border: none;
                padding: 7px;
                font-weight: 700;
            }
            QTableWidget { alternate-background-color: #1f252e; selection-background-color: #257c75; }
            QTextEdit { selection-background-color: #257c75; }
            QComboBox::drop-down { border: none; width: 24px; }
            QPushButton {
                background: #257c75;
                border: none;
                color: white;
                padding: 10px 14px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background: #2f938b; }
            QPushButton:disabled { background: #303741; color: #81909d; }
            QStatusBar { background: #191d24; color: #b7c5cf; }
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

    def _run_local_baseline(self) -> None:
        hardening = self.pages["Hardening"]
        profile_id = hardening.profile_combo.currentData() if hasattr(hardening, "profile_combo") else None
        if profile_id:
            self.controller.run_profile(profile_id)
            self.refresh_all()
