from __future__ import annotations

from pathlib import Path

from PySide6 import QtGui, QtWidgets

from hardsecnet_pyside.ui.pages import (
    AiAdvisorPage,
    BenchmarksPage,
    DashboardPage,
    HardeningPage,
    ReportsPage,
    SettingsPage,
)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.pages: dict[str, QtWidgets.QWidget] = {}
        self._configure_fonts()
        self._build_ui()
        self.refresh_all()

    def _configure_fonts(self) -> None:
        app = QtWidgets.QApplication.instance()
        if app is None:
            return

        font_family = "Arial"
        for font_path in (
            Path("C:/Windows/Fonts/arial.ttf"),
            Path("C:/Windows/Fonts/segoeui.ttf"),
            Path("C:/Windows/Fonts/calibri.ttf"),
        ):
            if not font_path.exists():
                continue
            font_id = QtGui.QFontDatabase.addApplicationFont(str(font_path))
            families = QtGui.QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font_family = families[0]
                break

        app.setFont(QtGui.QFont(font_family, 10))

    def _build_ui(self) -> None:
        self.setWindowTitle("HardSecNet - Local CIS Hardening Studio")
        self.setMinimumSize(1180, 760)
        root = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(root)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        self.nav = QtWidgets.QListWidget()
        self.nav.setObjectName("Navigation")
        self.nav.setFixedWidth(220)
        self.nav.addItems(
            ["Dashboard", "Hardening", "AI Advisor", "Reports", "Profile Builder", "Settings"]
        )
        self.nav.currentRowChanged.connect(self._select_page)

        self.stack = QtWidgets.QStackedWidget()
        self.pages = {
            "Dashboard": DashboardPage(self.controller, self.refresh_all),
            "Hardening": HardeningPage(self.controller, self.refresh_all),
            "AI Advisor": AiAdvisorPage(self.controller, self.refresh_all),
            "Reports": ReportsPage(self.controller, self.refresh_all),
            "Profile Builder": BenchmarksPage(self.controller, self.refresh_all),
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
        subtitle.setWordWrap(True)
        side.addWidget(title)
        side.addWidget(subtitle)
        side.addWidget(self.nav, 1)

        refresh_button = QtWidgets.QPushButton("Refresh All")
        refresh_button.setObjectName("SecondaryButton")
        refresh_button.clicked.connect(self.refresh_all)
        baseline_button = QtWidgets.QPushButton("Run Local Baseline")
        baseline_button.setObjectName("PrimaryButton")
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
            QMainWindow { background: #eef3f8; color: #182331; }
            QWidget { color: #182331; font-size: 13px; font-family: "Arial", "Segoe UI", sans-serif; }
            QFrame#Sidebar {
                background: #0e1726;
                border: 1px solid #223149;
                border-radius: 8px;
            }
            QLabel#AppTitle { font-size: 27px; font-weight: 900; color: #67e8d5; letter-spacing: 0px; }
            QLabel#AppSubtitle { color: #b8c7d9; margin-bottom: 10px; line-height: 130%; }
            QLabel#PageTitle { font-size: 27px; font-weight: 900; color: #0f172a; letter-spacing: 0px; }
            QLabel#PageSubtitle { color: #5b6b7f; margin-bottom: 8px; }
            QLabel#SectionTitle { color: #182537; font-size: 15px; font-weight: 900; }
            QLabel#PanelTitle { color: #111827; font-size: 16px; font-weight: 800; }
            QLabel#PanelText { color: #5b6b7d; }
            QListWidget#Navigation {
                background: #0b1322;
                border: 1px solid #253245;
                border-radius: 8px;
                padding: 7px;
                color: #e8eef7;
            }
            QListWidget#Navigation::item {
                padding: 11px 12px;
                margin: 4px;
                border-radius: 6px;
            }
            QListWidget#Navigation::item:selected {
                background: #f4c84f;
                color: #111827;
                font-weight: 800;
            }
            QListWidget#Navigation::item:hover { background: #1c2b42; }
            QFrame#MetricCard, QFrame#Panel {
                background: #ffffff;
                border: 1px solid #d7e0ec;
                border-radius: 8px;
            }
            QFrame#MetricCard[accent="cyan"] { border-top: 4px solid #16a3b8; }
            QFrame#MetricCard[accent="green"] { border-top: 4px solid #2f9e6d; }
            QFrame#MetricCard[accent="amber"] { border-top: 4px solid #c18a00; }
            QFrame#MetricCard[accent="coral"] { border-top: 4px solid #e05a47; }
            QFrame#MetricCard[accent="violet"] { border-top: 4px solid #7c5cff; }
            QFrame#MetricCard[accent="blue"] { border-top: 4px solid #2f75d6; }
            QLabel#MetricValue { font-size: 30px; font-weight: 900; color: #0f172a; }
            QLabel#MetricLabel { color: #243244; font-weight: 800; font-size: 13px; }
            QLabel#MetricCaption { color: #66758a; font-size: 12px; }
            QGroupBox {
                background: #ffffff;
                border: 1px solid #d7e0ec;
                border-radius: 8px;
                margin-top: 14px;
                padding: 12px;
                color: #1f2937;
                font-weight: 800;
            }
            QTableWidget, QTextEdit, QLineEdit, QComboBox {
                background: #ffffff;
                border: 1px solid #c9d5e4;
                border-radius: 8px;
                color: #172033;
                padding: 7px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border: 1px solid #1598a8;
            }
            QTableWidget::viewport, QTextEdit::viewport {
                background: #ffffff;
            }
            QAbstractScrollArea::corner {
                background: #edf2f7;
            }
            QHeaderView {
                background: #edf2f7;
                color: #243244;
            }
            QHeaderView::section {
                background: #e8eef6;
                color: #243244;
                border: none;
                padding: 8px;
                font-weight: 800;
            }
            QTableCornerButton::section {
                background: #edf2f7;
                border: none;
            }
            QTableWidget {
                alternate-background-color: #f7f9fc;
                selection-background-color: #d5f5ef;
                selection-color: #0f172a;
            }
            QTableWidget::item { padding-left: 4px; padding-right: 4px; }
            QTextEdit { selection-background-color: #d5f5ef; }
            QComboBox::drop-down { border: none; width: 24px; }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #edf2f7;
                border: 1px solid #ccd6e4;
                margin: 0px;
            }
            QScrollBar:vertical { width: 12px; }
            QScrollBar:horizontal { height: 12px; }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #99a9bd;
                border-radius: 5px;
                min-height: 28px;
                min-width: 28px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #74869c;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                width: 0px;
                height: 0px;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: transparent;
            }
            QPushButton {
                background: #126f8a;
                border: none;
                color: white;
                padding: 10px 14px;
                min-height: 18px;
                border-radius: 8px;
                font-weight: 800;
            }
            QPushButton:hover { background: #0f5c73; }
            QPushButton#PrimaryButton {
                background: #f4c84f;
                color: #111827;
            }
            QPushButton#PrimaryButton:hover { background: #e8bb3f; }
            QPushButton#SecondaryButton {
                background: #1d2a3d;
                color: #e8eef7;
                border: 1px solid #30435e;
            }
            QPushButton#SecondaryButton:hover { background: #263956; }
            QPushButton:disabled { background: #d5dde8; color: #8190a4; }
            QStatusBar {
                background: #e5edf6;
                color: #405064;
                border-top: 1px solid #d1dbe8;
            }
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
        control_count = len(self.controller.list_benchmark_items(os_family=device.os_family))
        self.statusBar().showMessage(
            f"{device.name} | {control_count} controls | {len(snapshot.runs)} runs | {len(snapshot.reports)} reports"
        )

    def _run_local_baseline(self) -> None:
        hardening = self.pages["Hardening"]
        profile_id = hardening.profile_combo.currentData() if hasattr(hardening, "profile_combo") else None
        if profile_id:
            self.controller.run_profile(profile_id)
            self.refresh_all()
