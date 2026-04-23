from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from PySide6 import QtCore, QtGui, QtWidgets


def _section(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName("SectionTitle")
    label.setContentsMargins(2, 10, 0, 2)
    return label


def _item(value: Any) -> QtWidgets.QTableWidgetItem:
    cell = QtWidgets.QTableWidgetItem("" if value is None else str(value))
    cell.setFlags(cell.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
    return cell


def _style_table(table: QtWidgets.QTableWidget) -> None:
    table_palette = table.palette()
    table_palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor("#ffffff"))
    table_palette.setColor(QtGui.QPalette.ColorRole.AlternateBase, QtGui.QColor("#f7f9fc"))
    table_palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("#ffffff"))
    table_palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor("#172033"))
    table.setPalette(table_palette)
    for header in (table.horizontalHeader(), table.verticalHeader()):
        header_palette = header.palette()
        header_palette.setColor(QtGui.QPalette.ColorRole.Base, QtGui.QColor("#edf2f7"))
        header_palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor("#edf2f7"))
        header_palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor("#edf2f7"))
        header_palette.setColor(QtGui.QPalette.ColorRole.Text, QtGui.QColor("#243244"))
        header.setPalette(header_palette)
        header.setAutoFillBackground(True)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setMinimumHeight(34)
    table.horizontalHeader().setDefaultAlignment(
        QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
    )
    table.verticalHeader().setDefaultSectionSize(34)
    table.setShowGrid(False)
    table.setMinimumHeight(150)
    table.setWordWrap(False)
    table.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)


def _fill(table: QtWidgets.QTableWidget, headers: list[str], rows: list[list[Any]]) -> None:
    _style_table(table)
    table.clear()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(rows))
    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            table.setItem(row_index, column_index, _item(value))
    table.resizeColumnsToContents()
    table.horizontalHeader().setStretchLastSection(True)


def _paint_status_column(table: QtWidgets.QTableWidget, column: int) -> None:
    palette = {
        "ready": ("#daf8ec", "#116149"),
        "completed": ("#daf8ec", "#116149"),
        "compliant": ("#daf8ec", "#116149"),
        "dry_run_recorded": ("#daf8ec", "#116149"),
        "review_required": ("#fff2c2", "#815b00"),
        "needs review": ("#fff2c2", "#815b00"),
        "review": ("#fff2c2", "#815b00"),
        "missing": ("#ffe1de", "#a33125"),
        "blocked": ("#ffe1de", "#a33125"),
        "failed": ("#ffe1de", "#a33125"),
        "high": ("#ffe1de", "#a33125"),
        "medium": ("#fff2c2", "#815b00"),
        "low": ("#daf8ec", "#116149"),
    }
    for row in range(table.rowCount()):
        cell = table.item(row, column)
        if cell is None:
            continue
        key = cell.text().strip().lower()
        colors = palette.get(key)
        if colors is None:
            continue
        background, foreground = colors
        cell.setBackground(QtGui.QBrush(QtGui.QColor(background)))
        cell.setForeground(QtGui.QBrush(QtGui.QColor(foreground)))
        font = cell.font()
        font.setBold(True)
        cell.setFont(font)


class BasePage(QtWidgets.QWidget):
    def __init__(self, title: str, subtitle: str = "") -> None:
        super().__init__()
        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setObjectName("PageTitle")
        self.subtitle_label = QtWidgets.QLabel(subtitle)
        self.subtitle_label.setObjectName("PageSubtitle")
        self.body = QtWidgets.QVBoxLayout()
        self.body.setSpacing(12)
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(2, 2, 2, 2)
        root.setSpacing(6)
        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addLayout(self.body)
        root.addStretch(1)


class MetricCard(QtWidgets.QFrame):
    def __init__(self, label: str, accent: str = "cyan") -> None:
        super().__init__()
        self.setObjectName("MetricCard")
        self.setProperty("accent", accent)
        self.setMinimumSize(168, 96)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(3)
        self.label = QtWidgets.QLabel(label)
        self.label.setObjectName("MetricLabel")
        self.label.setWordWrap(True)
        self.value = QtWidgets.QLabel("0")
        self.value.setObjectName("MetricValue")
        self.caption = QtWidgets.QLabel("")
        self.caption.setObjectName("MetricCaption")
        self.caption.setWordWrap(True)
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        layout.addWidget(self.caption)

    def set_value(self, value: Any) -> None:
        self.value.setText(str(value))

    def set_caption(self, value: str) -> None:
        self.caption.setText(value)


class DashboardPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__(
            "Dashboard",
            "Current-device hardening posture, open findings, drift, and evidence status.",
        )
        self.controller = controller
        self.on_refresh = on_refresh
        self.profile_combo = QtWidgets.QComboBox()
        self.selected_profile_id: str | None = None
        self.cards = {
            "score": MetricCard("Compliance Score", "green"),
            "open": MetricCard("Open Findings", "amber"),
            "ready": MetricCard("Ready Actions", "cyan"),
            "last_run": MetricCard("Last Run", "blue"),
            "drift": MetricCard("Drift Changes", "coral"),
            "reports": MetricCard("Reports Ready", "violet"),
        }
        card_grid = QtWidgets.QGridLayout()
        card_grid.setSpacing(10)
        for index, card in enumerate(self.cards.values()):
            card_grid.addWidget(card, 0, index)
        card_area = QtWidgets.QWidget()
        card_area.setFixedHeight(118)
        card_area.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Fixed,
        )
        card_area.setLayout(card_grid)

        self.device_panel = QtWidgets.QFrame()
        self.device_panel.setObjectName("Panel")
        device_layout = QtWidgets.QVBoxLayout(self.device_panel)
        device_layout.setContentsMargins(14, 12, 14, 12)
        self.device_label = QtWidgets.QLabel()
        self.device_label.setObjectName("PanelTitle")
        self.device_detail = QtWidgets.QLabel()
        self.device_detail.setObjectName("PanelText")
        self.device_detail.setWordWrap(True)
        device_layout.addWidget(self.device_label)
        device_layout.addWidget(self.device_detail)

        self.summary = QtWidgets.QTextEdit()
        self.summary.setReadOnly(True)
        self.summary.setMinimumHeight(120)
        self.latest_table = QtWidgets.QTableWidget()
        self.drift_table = QtWidgets.QTableWidget()

        run_button = QtWidgets.QPushButton("Run Local Profile")
        run_button.clicked.connect(self._run_profile)
        actions = QtWidgets.QHBoxLayout()
        actions.addWidget(QtWidgets.QLabel("Profile"))
        actions.addWidget(self.profile_combo, 1)
        actions.addWidget(run_button)
        actions.addStretch(1)

        self.body.addWidget(card_area)
        self.body.addWidget(self.device_panel)
        self.body.addLayout(actions)
        self.body.addWidget(_section("Priority Findings"))
        self.body.addWidget(self.latest_table)
        self.body.addWidget(_section("Drift Since Previous Run"))
        self.body.addWidget(self.drift_table)
        self.body.addWidget(_section("Operator Summary"))
        self.body.addWidget(self.summary)

    def refresh(self) -> None:
        snapshot = self.controller.dashboard_snapshot()
        device = snapshot["device"]
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        for profile in self.controller.list_profiles(device.os_family):
            self.profile_combo.addItem(profile.name, profile.id)
            if profile.id == self.selected_profile_id:
                self.profile_combo.setCurrentIndex(self.profile_combo.count() - 1)
        self.profile_combo.blockSignals(False)
        runs = snapshot["runs"]
        latest_run = runs[0] if runs else None
        findings = snapshot["findings"]
        comparisons = snapshot["comparisons"]
        total_controls = len(snapshot["items"])
        compliant_count = sum(1 for item in findings if item.status.lower() == "compliant")
        open_findings = [item for item in findings if item.status.lower() != "compliant"]
        open_count = len(open_findings)
        score = round((compliant_count / len(findings)) * 100) if findings else 0
        readiness = self.controller.list_script_readiness(os_family=device.os_family)
        ready_count = sum(1 for item in readiness if item.status == "ready")

        self.cards["score"].set_value(f"{score}%")
        self.cards["open"].set_value(open_count)
        self.cards["ready"].set_value(ready_count)
        self.cards["last_run"].set_value("OK" if latest_run else "None")
        self.cards["drift"].set_value(len(comparisons))
        self.cards["reports"].set_value(len(snapshot["reports"]))
        self.cards["score"].set_caption(f"{compliant_count}/{len(findings) or total_controls} controls compliant")
        self.cards["open"].set_caption("Non-compliant or review-required controls")
        self.cards["ready"].set_caption("Approved scripts available for this OS")
        self.cards["last_run"].set_caption(latest_run.ended_at if latest_run and latest_run.ended_at else "Run a profile to populate posture")
        self.cards["drift"].set_caption("Status changes since prior run")
        self.cards["reports"].set_caption("Exportable JSON, HTML, and PDF evidence")

        self.device_label.setText(f"{device.name} | {device.os_family}")
        self.device_detail.setText(
            f"{device.hostname} | {total_controls} loaded controls | "
            f"{len(snapshot['modules'])} modules | {len(snapshot['profiles'])} local profiles | "
            f"{len(readiness)} script mappings"
        )

        priority_findings = sorted(
            open_findings,
            key=lambda item: (
                {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(item.severity.lower(), 0),
                item.benchmark_id,
            ),
            reverse=True,
        )
        _fill(
            self.latest_table,
            ["Benchmark", "Severity", "Status", "Action"],
            [
                [
                    item.benchmark_id,
                    item.severity,
                    item.status,
                    "; ".join(item.remediation) if item.remediation else item.title,
                ]
                for item in priority_findings[:8]
            ],
        )
        _paint_status_column(self.latest_table, 1)
        _paint_status_column(self.latest_table, 2)
        _fill(
            self.drift_table,
            ["Benchmark", "Change", "Before", "After"],
            [
                [delta.benchmark_id, delta.delta_type, delta.before_status, delta.after_status]
                for delta in comparisons[:8]
            ],
        )

        if latest_run is None:
            self.summary.setPlainText(
                "No local run has been recorded yet.\n"
                "Run a local profile to calculate compliance score, open findings, drift, and report readiness."
            )
            return
        report = snapshot["latest_report"]
        self.summary.setPlainText(
            "\n".join(
                [
                    f"Device: {device.name} ({device.hostname})",
                    f"Latest run: {latest_run.id} [{latest_run.status}]",
                    f"Profile: {latest_run.profile_id}",
                    f"Compliance: {score}% ({compliant_count}/{len(findings)} controls compliant)",
                    f"Open findings: {open_count}",
                    f"Ready hardening actions: {ready_count}",
                    f"Drift changes: {len(comparisons)}",
                    f"Latest report: {report.title if report else 'not generated'}",
                ]
            )
        )

    def _run_profile(self) -> None:
        profile_id = self.profile_combo.currentData()
        if not profile_id:
            return
        self.selected_profile_id = str(profile_id)
        self.controller.run_profile(profile_id)
        self.on_refresh()


class HardeningPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__(
            "Run Center",
            "Select a profile, run the audit, review findings, and optionally apply ready hardening scripts.",
        )
        self.controller = controller
        self.on_refresh = on_refresh
        self.profile_combo = QtWidgets.QComboBox()
        self.device_label = QtWidgets.QLabel()
        self.module_table = QtWidgets.QTableWidget()
        self.run_table = QtWidgets.QTableWidget()
        self.finding_table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        self.selected_profile_id: str | None = None

        run_button = QtWidgets.QPushButton("Run Profile")
        run_button.clicked.connect(self._run_profile)
        check_button = QtWidgets.QPushButton("Check Ready Settings")
        check_button.clicked.connect(self._check_ready_script_status)
        harden_button = QtWidgets.QPushButton("Harden Ready Settings")
        harden_button.clicked.connect(self._harden_ready_script)
        rollback_button = QtWidgets.QPushButton("Deharden Ready Settings")
        rollback_button.clicked.connect(self._rollback_ready_script)

        header = QtWidgets.QHBoxLayout()
        header.addWidget(QtWidgets.QLabel("Profile"))
        header.addWidget(self.profile_combo, 1)
        header.addWidget(run_button)
        header.addWidget(check_button)
        header.addWidget(harden_button)
        header.addWidget(rollback_button)

        device_group = QtWidgets.QGroupBox("Target System")
        device_form = QtWidgets.QFormLayout(device_group)
        device_form.addRow("This machine", self.device_label)

        self.module_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.run_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.finding_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.run_table.itemSelectionChanged.connect(self._show_run_details)
        self.profile_combo.currentIndexChanged.connect(self._on_profile_changed)

        self.body.addLayout(header)
        self.body.addWidget(device_group)
        self.body.addWidget(_section("What This Profile Runs"))
        self.body.addWidget(self.module_table)
        self.body.addWidget(_section("Run History"))
        self.body.addWidget(self.run_table)
        self.body.addWidget(_section("Findings From Latest Run"))
        self.body.addWidget(self.finding_table)
        self.body.addWidget(_section("Selected Run Details"))
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        device = self.controller.get_current_device()
        self.device_label.setText(f"{device.name} ({device.hostname}) - {device.os_family}")

        current_profile_id = self.selected_profile_id or (
            str(self.profile_combo.currentData()) if self.profile_combo.currentData() else None
        )
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        for profile in self.controller.list_profiles(device.os_family):
            self.profile_combo.addItem(profile.name, profile.id)
        if self.profile_combo.count() == 0:
            for profile in self.controller.list_profiles():
                self.profile_combo.addItem(profile.name, profile.id)
        if current_profile_id:
            index = self.profile_combo.findData(current_profile_id)
            if index >= 0:
                self.profile_combo.setCurrentIndex(index)
        self.profile_combo.blockSignals(False)

        runs = self.controller.list_runs(device.id)
        _fill(
            self.run_table,
            ["Run", "Profile", "Status", "Started", "Ended"],
            [[run.id, run.profile_id, run.status, run.started_at, run.ended_at or ""] for run in runs],
        )

        latest_run = runs[0] if runs else None
        findings = self.controller.list_findings(latest_run.id) if latest_run else []
        _fill(
            self.finding_table,
            ["Benchmark", "Title", "Status", "Severity", "Confidence"],
            [[item.benchmark_id, item.title, item.status, item.severity, f"{item.confidence:.2f}"] for item in findings],
        )
        _paint_status_column(self.finding_table, 2)
        self._on_profile_changed()

    def _run_profile(self) -> None:
        profile_id = self.profile_combo.currentData()
        if not profile_id:
            return
        self.controller.run_profile(profile_id)
        self.on_refresh()

    def _harden_ready_script(self) -> None:
        ready = self._ready_scripts_for_selected_profile()
        if not ready:
            self.details.setPlainText("No ready script is available for the current device OS.")
            return
        executions = [self.controller.run_script_dry_run(item.item_id, execute=True) for item in ready]
        self.details.setPlainText(
            "\n".join(
                [
                    f"Demo action: harden {len(executions)} ready setting(s) in the selected profile.",
                    "",
                    *self._format_script_executions(executions),
                ]
            )
        )

    def _check_ready_script_status(self) -> None:
        ready = self._ready_scripts_for_selected_profile()
        if not ready:
            self.details.setPlainText("No ready script is available for the current device OS.")
            return
        executions = [self.controller.check_script_status(item.item_id) for item in ready]
        self.details.setPlainText(
            "\n".join(
                [
                    f"Demo check: current state for {len(executions)} ready setting(s) in this profile.",
                    "",
                    *self._format_script_executions(executions),
                ]
            )
        )

    def _rollback_ready_script(self) -> None:
        ready = self._ready_scripts_for_selected_profile()
        if not ready:
            self.details.setPlainText("No ready script is available for the current device OS.")
            return
        executions = [self.controller.rollback_script(item.item_id) for item in ready]
        self.details.setPlainText(
            "\n".join(
                [
                    f"Demo setup: deharden {len(executions)} ready setting(s) so before/after changes are visible.",
                    "",
                    *self._format_script_executions(executions),
                ]
            )
        )

    def _ready_scripts_for_selected_profile(self):
        device = self.controller.get_current_device()
        profile_id = self.profile_combo.currentData()
        profile = self.controller.repository.get_profile(profile_id) if profile_id else None
        allowed = set(profile.benchmark_ids) if profile and profile.benchmark_ids else set()
        ready = [
            item
            for item in self.controller.list_script_readiness(os_family=device.os_family)
            if item.status == "ready" and (not allowed or item.benchmark_id in allowed)
        ]
        return ready

    def _on_profile_changed(self) -> None:
        profile_id = self.profile_combo.currentData()
        self.selected_profile_id = str(profile_id) if profile_id else None
        self._refresh_profile_details()

    def _refresh_profile_details(self) -> None:
        device = self.controller.get_current_device()
        profile_id = self.profile_combo.currentData()
        profile = self.controller.repository.get_profile(profile_id) if profile_id else None
        modules = [
            module for module in self.controller.list_modules(device.os_family)
            if profile is None or module.id in profile.module_ids
        ]
        _fill(
            self.module_table,
            ["Module", "Purpose", "Enabled"],
            [[module.name, module.description, "Yes"] for module in modules],
        )

        ready = self._ready_scripts_for_selected_profile()
        if profile is None:
            self.details.setPlainText("No profile selected.")
            return

        self.run_table.clearSelection()
        self.details.setPlainText(
            "\n".join(
                [
                    f"Profile: {profile.name}",
                    f"Profile ID: {profile.id}",
                    f"Description: {profile.description}",
                    f"Modules in scope: {len(profile.module_ids)}",
                    f"Benchmarks in scope: {len(profile.benchmark_ids)}",
                    f"Ready scripts in scope: {len(ready)}",
                ]
            )
        )

    def _format_script_executions(self, executions) -> list[str]:
        lines: list[str] = []
        for execution in executions:
            display_status = self._display_execution_status(execution)
            output = self._display_execution_output(execution)
            error = self._display_execution_error(execution)
            lines.extend(
                [
                    f"Benchmark: {execution.benchmark_id}",
                    f"Execution: {execution.id} | {execution.mode} | {display_status}",
                    f"Output:\n{output or 'none'}",
                    f"Error: {error or 'none'}",
                    f"Artifact: {execution.artifact_path}",
                    "",
                ]
            )
        return lines

    def _display_execution_status(self, execution) -> str:
        if execution.status == "blocked" and "requires an elevated Administrator session" in (execution.error or ""):
            return "Admin Required"
        return execution.status

    def _display_execution_output(self, execution) -> str:
        output = execution.output or ""
        if execution.mode == "status" and "Status: OFF" in output:
            return output.replace("Status: OFF", "Status: Not Hardened Yet")
        return output

    def _display_execution_error(self, execution) -> str:
        error = execution.error or ""
        if execution.status == "blocked" and "requires an elevated Administrator session" in error:
            return "Run the app from an Administrator terminal to check or apply this control."
        return error

    def _show_run_details(self) -> None:
        selected = self.run_table.selectedItems()
        if not selected:
            run = self.controller.list_runs(self.controller.get_current_device().id)[0] if self.controller.list_runs(self.controller.get_current_device().id) else None
        else:
            run = self.controller.repository.get_run(selected[0].text())
        if run is None:
            self.details.setPlainText("No runs available yet.")
            return
        report = self.controller.latest_report(run.id)
        self.details.setPlainText(
            "\n".join(
                [
                    f"Run: {run.id}",
                    f"Profile: {run.profile_id}",
                    f"Status: {run.status}",
                    f"Modules: {', '.join(run.modules) or 'none'}",
                    f"Report JSON: {report.json_path if report else 'not generated'}",
                ]
            )
        )


class NetworkPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Network", "Review network posture checks and drift movement.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        refresh = QtWidgets.QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        self.table.itemSelectionChanged.connect(self._show_details)
        self.body.addWidget(refresh)
        self.body.addWidget(self.table)
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        checks = self.controller.get_network_checks()
        _fill(
            self.table,
            ["Title", "Status", "Details", "Benchmarks"],
            [[check.title, check.status, check.details, ", ".join(check.benchmark_refs)] for check in checks],
        )
        self._show_details()

    def _show_details(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            self.details.setPlainText("Select a row to inspect the network check.")
            return
        self.details.setPlainText(
            f"{selected[0].text()}\nStatus: {selected[1].text()}\nDetails: {selected[2].text()}"
        )


class AiAdvisorPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("AI Advisor", "Check Ollama status and review risk explanations for latest findings.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.status_label = QtWidgets.QLabel()
        self.status_label.setObjectName("PanelTitle")
        self.table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        refresh = QtWidgets.QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        self.table.itemSelectionChanged.connect(self._show_details)
        self.body.addWidget(self.status_label)
        self.body.addWidget(refresh)
        self.body.addWidget(self.table)
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        status = self.controller.ollama_status()
        badge = "CONNECTED" if status["connected"] else "OFFLINE"
        self.status_label.setText(
            f"Ollama: {badge} | Model: {status['model']} | {status['message']}"
        )
        snapshot = self.controller.get_dashboard_snapshot()
        run = snapshot.runs[0] if snapshot.runs else None
        if run is None:
            _fill(self.table, ["Benchmark", "Severity", "Status", "Explanation"], [])
            self.details.setPlainText("Run a profile first. Findings will appear here with risk and remediation explanations.")
            return
        findings = self.controller.list_findings(run.id)
        recommendations = {
            item.benchmark_reference: item for item in self.controller.ai_recommendations(run.id)
        }
        _fill(
            self.table,
            ["Benchmark", "Severity", "Status", "Explanation"],
            [
                [
                    finding.benchmark_id,
                    finding.severity,
                    finding.status,
                    recommendations.get(finding.benchmark_id).explanation
                    if recommendations.get(finding.benchmark_id)
                    else finding.rationale or finding.title,
                ]
                for finding in findings
            ],
        )
        if self.table.rowCount() > 0:
            self.table.selectRow(0)
        _paint_status_column(self.table, 1)
        _paint_status_column(self.table, 2)
        self._show_details()

    def _show_details(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            self.details.setPlainText("Select a finding to inspect its risk explanation and remediation context.")
            return
        benchmark_id = selected[0].text()
        run = self.controller.latest_run()
        finding = None
        if run is not None:
            finding = next(
                (item for item in self.controller.list_findings(run.id) if item.benchmark_id == benchmark_id),
                None,
            )
        if finding is None:
            self.details.setPlainText("Finding metadata could not be resolved.")
            return
        rec = next(
            (
                item
                for item in self.controller.ai_recommendations(run.id if run else None)
                if item.benchmark_reference == benchmark_id
            ),
            None,
        )
        self.details.setPlainText(
            "\n".join(
                [
                    f"Benchmark: {finding.benchmark_id}",
                    f"Title: {finding.title}",
                    f"Status: {finding.status}",
                    f"Severity: {finding.severity}",
                    f"Risk explanation: {(rec.explanation if rec else finding.rationale) or 'No explanation recorded yet.'}",
                    f"Recommended action: {(rec.proposed_action if rec else '; '.join(finding.remediation)) or 'Review benchmark guidance.'}",
                    f"Expected impact: {(rec.expected_impact if rec else finding.expected) or 'Reduce benchmark drift.'}",
                    f"Rollback: {(rec.rollback_path if rec else '; '.join(finding.rollback)) or 'Review generated script notes.'}",
                ]
            )
        )


class ReportsPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Reports", "Exported JSON, HTML, and PDF artifacts for each completed run.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        refresh = QtWidgets.QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)
        open_html = QtWidgets.QPushButton("Open HTML")
        open_html.clicked.connect(lambda: self._open_selected("html"))
        open_pdf = QtWidgets.QPushButton("Open PDF")
        open_pdf.clicked.connect(lambda: self._open_selected("pdf"))
        actions = QtWidgets.QHBoxLayout()
        actions.addWidget(refresh)
        actions.addWidget(open_html)
        actions.addWidget(open_pdf)
        actions.addStretch(1)
        self.table.itemSelectionChanged.connect(self._show_details)
        self.body.addLayout(actions)
        self.body.addWidget(self.table)
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        reports = self.controller.list_reports()
        _fill(
            self.table,
            ["Title", "Run", "Generated", "JSON", "HTML", "PDF"],
            [
                [
                    report.title,
                    report.run_id,
                    report.generated_at,
                    Path(report.json_path).name,
                    Path(report.html_path).name,
                    Path(report.pdf_path).name if report.pdf_path else "",
                ]
                for report in reports
            ],
        )
        if self.table.rowCount() > 0:
            self.table.selectRow(0)
        self._show_details()

    def _show_details(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            self.details.setPlainText("Select a report to inspect its artifact paths.")
            return
        report_id = None
        for report in self.controller.list_reports():
            if report.title == selected[0].text() and report.run_id == selected[1].text():
                report_id = report.id
                break
        if report_id is None:
            self.details.setPlainText("Report metadata could not be resolved.")
            return
        payload = self.controller.export_report_payload(report_id)
        report = payload["report"]
        findings = payload["findings"]
        open_findings = [item for item in findings if item["status"] != "Compliant"]
        self.details.setPlainText(
            "\n".join(
                [
                    f"Report: {payload['report']['title']}",
                    f"Run: {payload['run']['id']}",
                    f"Findings: {len(payload['findings'])}",
                    f"Open findings: {len(open_findings)}",
                    f"Comparisons: {len(payload['comparisons'])}",
                    f"Device: {payload['device']['name']}",
                    f"JSON: {report['json_path']}",
                    f"HTML: {report['html_path']}",
                    f"PDF: {report['pdf_path']}",
                    "",
                    "Top findings:",
                    *[
                        f"- {item['benchmark_id']} | {item['severity']} | {item['status']} | {item['title']}"
                        for item in open_findings[:8]
                    ],
                ]
            )
        )

    def _selected_report(self):
        selected = self.table.selectedItems()
        if not selected:
            return None
        for report in self.controller.list_reports():
            if report.title == selected[0].text() and report.run_id == selected[1].text():
                return report
        return None

    def _open_selected(self, artifact: str) -> None:
        report = self._selected_report()
        if report is None:
            self.details.setPlainText("Select a report first.")
            return
        path = Path(report.html_path if artifact == "html" else report.pdf_path)
        if not path.exists():
            self.details.setPlainText(f"{artifact.upper()} artifact does not exist: {path}")
            return
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(path)))


class BenchmarksPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Profile Builder", "Select CIS controls and save them as a hardening profile.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.current_documents: list[Any] = []
        self.current_items: list[Any] = []
        self.current_readiness: list[Any] = []
        self.selected_benchmark_ids: list[str] = []
        self.path_edit = QtWidgets.QLineEdit()
        self.documents_table = QtWidgets.QTableWidget()
        self.items_table = QtWidgets.QTableWidget()
        self.selection_table = QtWidgets.QTableWidget()
        self.readiness_table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)
        self.profile_name = QtWidgets.QLineEdit()
        self.profile_name.setPlaceholderText("Profile name, e.g. Windows Demo Hardening")
        self.profile_name.setMinimumWidth(220)
        self.strictness_combo = QtWidgets.QComboBox()
        self.strictness_combo.addItems(["balanced", "audit_only", "strict"])

        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self._browse)
        import_button = QtWidgets.QPushButton("Import Benchmark")
        import_button.clicked.connect(self._import)
        add_button = QtWidgets.QPushButton("Add Selected Controls")
        add_button.clicked.connect(self._add_selected_items)
        remove_button = QtWidgets.QPushButton("Remove Highlighted")
        remove_button.clicked.connect(self._remove_selected_items)
        clear_button = QtWidgets.QPushButton("Clear Profile Selection")
        clear_button.clicked.connect(self._clear_selected_items)
        dry_run_button = QtWidgets.QPushButton("Dry Run Selected Script")
        dry_run_button.clicked.connect(self._dry_run_selected_script)
        harden_button = QtWidgets.QPushButton("Harden Selected Script")
        harden_button.clicked.connect(self._harden_selected_script)
        rollback_button = QtWidgets.QPushButton("Deharden Selected Script")
        rollback_button.clicked.connect(self._rollback_selected_script)
        save_profile = QtWidgets.QPushButton("Save Selected As Profile")
        save_profile.clicked.connect(self._save_selected_profile)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.path_edit, 1)
        row.addWidget(browse)
        row.addWidget(import_button)

        selection_actions = QtWidgets.QHBoxLayout()
        selection_actions.addWidget(add_button)
        selection_actions.addWidget(remove_button)
        selection_actions.addWidget(clear_button)
        selection_actions.addStretch(1)

        script_actions = QtWidgets.QHBoxLayout()
        script_actions.addWidget(self.profile_name, 1)
        script_actions.addWidget(self.strictness_combo)
        script_actions.addWidget(save_profile)
        script_actions.addWidget(dry_run_button)
        script_actions.addWidget(harden_button)
        script_actions.addWidget(rollback_button)

        self.documents_table.itemSelectionChanged.connect(self._show_items)
        self.items_table.itemSelectionChanged.connect(self._show_item_details)
        self.selection_table.itemSelectionChanged.connect(self._show_selected_item_details)
        self.readiness_table.itemSelectionChanged.connect(self._show_script_details)
        self.body.addLayout(row)
        self.body.addWidget(_section("Loaded CIS Benchmark Sets"))
        self.body.addWidget(self.documents_table)
        self.body.addWidget(_section("CIS Controls In Selected Set"))
        self.body.addWidget(self.items_table)
        self.body.addLayout(selection_actions)
        self.body.addWidget(_section("Controls In Profile"))
        self.body.addWidget(self.selection_table)
        self.body.addWidget(_section("Profile Builder And Script Readiness"))
        self.body.addLayout(script_actions)
        self.body.addWidget(self.readiness_table)
        self.body.addWidget(_section("Details"))
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        device = self.controller.get_current_device()
        self.current_documents = self.controller.list_benchmark_documents(device.os_family)
        _fill(
            self.documents_table,
            ["Name", "Version", "OS", "Controls", "Source"],
            [
                [
                    doc.name,
                    doc.version,
                    doc.os_family,
                    len(self.controller.list_benchmark_items(doc.id)),
                    doc.source_type,
                ]
                for doc in self.current_documents
            ],
        )
        if self.documents_table.rowCount() > 0 and self.documents_table.currentRow() < 0:
            self.documents_table.selectRow(0)
        self._show_items()

    def _browse(self) -> None:
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Import benchmark",
            "",
            "Benchmark files (*.json *.xml *.xccdf *.oval *.pdf *.txt);;All files (*.*)",
        )
        if file_name:
            self.path_edit.setText(file_name)

    def _import(self) -> None:
        source = self.path_edit.text().strip()
        if not source:
            self.details.setPlainText("Provide a benchmark file path before importing.")
            return
        self.controller.import_benchmark(source)
        self.on_refresh()

    def _show_items(self) -> None:
        device = self.controller.get_current_device()
        self.current_documents = self.controller.list_benchmark_documents(device.os_family)
        if not self.current_documents:
            _fill(self.items_table, ["Benchmark", "Title", "Status", "Confidence"], [])
            _fill(self.readiness_table, ["Benchmark", "Readiness", "Risk", "Script", "Reason"], [])
            self.details.setPlainText("No benchmark documents are available.")
            return
        row = self.documents_table.currentRow()
        document = self.current_documents[min(max(row, 0), len(self.current_documents) - 1)]
        self.current_items = self.controller.list_benchmark_items(document.id)
        self.current_readiness = self.controller.list_script_readiness(document.id)
        _fill(
            self.items_table,
            ["Benchmark", "Title", "Level", "Script", "Confidence"],
            [
                [
                    item.benchmark_id,
                    item.title,
                    item.profile_level,
                    item.script_state,
                    f"{item.confidence:.2f}",
                ]
                for item in self.current_items
            ],
        )
        self.items_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.items_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        _fill(
            self.readiness_table,
            ["Benchmark", "Readiness", "Risk", "Script", "Reason"],
            [
                [
                    item.benchmark_id,
                    item.status,
                    item.risk_level,
                    Path(item.script_path).name if item.script_path else "",
                    item.reason,
                ]
                for item in self.current_readiness
            ],
        )
        _paint_status_column(self.readiness_table, 1)
        _paint_status_column(self.readiness_table, 2)
        self._refresh_selected_controls_table()
        self.details.setPlainText(
            f"Document: {document.name}\nVersion: {document.version}\nSource: {document.source_path}\n"
            f"Controls loaded: {len(self.current_items)}\nScripts: {self._script_readiness_summary()}\n"
            f"Selected for profile: {len(self.selected_benchmark_ids)}\n"
            "Add controls into the profile selection, remove them if needed, then click Save Selected As Profile."
        )

    def _show_item_details(self) -> None:
        selected = self.items_table.selectedItems()
        if not selected:
            return
        self.details.append(
            "\n\nSelected item:\n"
            f"- Benchmark: {selected[0].text()}\n"
            f"- Title: {selected[1].text()}\n"
            f"- Level: {selected[2].text()}\n"
            f"- Script: {selected[3].text()}\n"
            f"- Confidence: {selected[4].text()}"
        )

    def _show_selected_item_details(self) -> None:
        row = self.selection_table.currentRow()
        if row < 0:
            return
        benchmark_id_item = self.selection_table.item(row, 0)
        if benchmark_id_item is None:
            return
        benchmark_id = benchmark_id_item.text()
        item = next((entry for entry in self.current_items if entry.benchmark_id == benchmark_id), None)
        if item is None:
            return
        self.details.setPlainText(
            "\n".join(
                [
                    f"Selected benchmark: {item.benchmark_id}",
                    f"Title: {item.title}",
                    f"Level: {item.profile_level}",
                    f"Script state: {item.script_state}",
                    f"Confidence: {item.confidence:.2f}",
                    f"Currently in profile: yes ({len(self.selected_benchmark_ids)} total)",
                ]
            )
        )

    def _show_script_details(self) -> None:
        readiness = self._selected_readiness()
        if readiness is None:
            return
        executions = self.controller.list_script_executions(readiness.item_id)
        latest = executions[0] if executions else None
        self.details.setPlainText(
            "\n".join(
                [
                    f"Benchmark: {readiness.benchmark_id}",
                    f"Title: {readiness.title}",
                    f"Readiness: {readiness.status}",
                    f"Risk: {readiness.risk_level}",
                    f"Script: {readiness.script_path or 'missing'}",
                    f"Reason: {readiness.reason}",
                    f"Commands: {', '.join(readiness.commands_preview) if readiness.commands_preview else 'none'}",
                    f"Rollback: {', '.join(readiness.rollback_notes) if readiness.rollback_notes else 'review benchmark notes'}",
                    f"Latest execution: {latest.status if latest else 'none'}",
                    f"Artifact: {latest.artifact_path if latest else 'none'}",
                ]
            )
        )

    def _dry_run_selected_script(self) -> None:
        readiness = self._selected_readiness()
        if readiness is None:
            row = self.items_table.currentRow()
            if 0 <= row < len(self.current_items):
                item = self.current_items[row]
                matches = [entry for entry in self.current_readiness if entry.item_id == item.id]
                readiness = matches[0] if matches else None
        if readiness is None:
            self.details.setPlainText("Select a benchmark item or script readiness row first.")
            return
        execution = self.controller.run_script_dry_run(readiness.item_id)
        self._show_items()
        self._select_readiness_by_item_id(readiness.item_id)
        self.details.setPlainText(
            "\n".join(
                [
                    f"Dry run: {execution.id}",
                    f"Benchmark: {execution.benchmark_id}",
                    f"Status: {execution.status}",
                    f"Readiness: {execution.readiness_status}",
                    f"Risk: {execution.risk_level}",
                    f"Command: {execution.command or 'none'}",
                    f"Output: {execution.output or 'none'}",
                    f"Error: {execution.error or 'none'}",
                    f"Artifact: {execution.artifact_path}",
                ]
            )
        )

    def _harden_selected_script(self) -> None:
        readiness = self._selected_readiness()
        if readiness is None:
            row = self.items_table.currentRow()
            if 0 <= row < len(self.current_items):
                item = self.current_items[row]
                matches = [entry for entry in self.current_readiness if entry.item_id == item.id]
                readiness = matches[0] if matches else None
        if readiness is None:
            self.details.setPlainText("Select a benchmark item or script readiness row first.")
            return
        execution = self.controller.run_script_dry_run(readiness.item_id, execute=True)
        self._show_items()
        self._select_readiness_by_item_id(readiness.item_id)
        self.details.setPlainText(
            "\n".join(
                [
                    f"Harden execution: {execution.id}",
                    f"Benchmark: {execution.benchmark_id}",
                    f"Status: {execution.status}",
                    f"Readiness: {execution.readiness_status}",
                    f"Risk: {execution.risk_level}",
                    f"Command: {execution.command or 'none'}",
                    f"Output: {execution.output or 'none'}",
                    f"Error: {execution.error or 'none'}",
                    f"Artifact: {execution.artifact_path}",
                ]
            )
        )

    def _rollback_selected_script(self) -> None:
        readiness = self._selected_readiness()
        if readiness is None:
            row = self.items_table.currentRow()
            if 0 <= row < len(self.current_items):
                item = self.current_items[row]
                matches = [entry for entry in self.current_readiness if entry.item_id == item.id]
                readiness = matches[0] if matches else None
        if readiness is None:
            self.details.setPlainText("Select a benchmark item or script readiness row first.")
            return
        execution = self.controller.rollback_script(readiness.item_id)
        self._show_items()
        self._select_readiness_by_item_id(readiness.item_id)
        self.details.setPlainText(
            "\n".join(
                [
                    f"Deharden execution: {execution.id}",
                    f"Benchmark: {execution.benchmark_id}",
                    f"Status: {execution.status}",
                    f"Readiness: {execution.readiness_status}",
                    f"Risk: {execution.risk_level}",
                    f"Command: {execution.command or 'none'}",
                    f"Output: {execution.output or 'none'}",
                    f"Error: {execution.error or 'none'}",
                    f"Artifact: {execution.artifact_path}",
                ]
            )
        )

    def _selected_readiness(self):
        row = self.readiness_table.currentRow()
        if 0 <= row < len(self.current_readiness):
            return self.current_readiness[row]
        return None

    def _selected_item_rows(self) -> list[int]:
        return sorted({item.row() for item in self.items_table.selectedItems()})

    def _add_selected_items(self) -> None:
        rows = self._selected_item_rows()
        if not rows:
            self.details.setPlainText("Select one or more controls in the benchmark table first.")
            return
        added = 0
        for row in rows:
            if 0 <= row < len(self.current_items):
                benchmark_id = self.current_items[row].benchmark_id
                if benchmark_id not in self.selected_benchmark_ids:
                    self.selected_benchmark_ids.append(benchmark_id)
                    added += 1
        self._refresh_selected_controls_table()
        self.details.setPlainText(
            f"Added {added} control(s) to the profile selection. Selected now: {len(self.selected_benchmark_ids)}."
        )

    def _remove_selected_items(self) -> None:
        rows = sorted({item.row() for item in self.selection_table.selectedItems()}, reverse=True)
        if not rows:
            self.details.setPlainText("Highlight one or more controls in the profile selection table first.")
            return
        removed = 0
        for row in rows:
            item = self.selection_table.item(row, 0)
            if item is None:
                continue
            benchmark_id = item.text()
            if benchmark_id in self.selected_benchmark_ids:
                self.selected_benchmark_ids.remove(benchmark_id)
                removed += 1
        self._refresh_selected_controls_table()
        self.details.setPlainText(
            f"Removed {removed} control(s) from the profile selection. Selected now: {len(self.selected_benchmark_ids)}."
        )

    def _clear_selected_items(self) -> None:
        self.selected_benchmark_ids.clear()
        self._refresh_selected_controls_table()
        self.details.setPlainText("Cleared the current profile selection.")

    def _refresh_selected_controls_table(self) -> None:
        selected_items = [
            item for item in self.current_items if item.benchmark_id in set(self.selected_benchmark_ids)
        ]
        _fill(
            self.selection_table,
            ["Benchmark", "Title", "Level", "Script"],
            [
                [item.benchmark_id, item.title, item.profile_level, item.script_state]
                for item in selected_items
            ],
        )
        self.selection_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.selection_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

    def _select_readiness_by_item_id(self, item_id: str) -> None:
        for row, item in enumerate(self.current_readiness):
            if item.item_id == item_id:
                self.readiness_table.selectRow(row)
                return

    def _script_readiness_summary(self) -> str:
        if not self.current_readiness:
            return "none"
        counts: dict[str, int] = {}
        for item in self.current_readiness:
            counts[item.status] = counts.get(item.status, 0) + 1
        return ", ".join(f"{status}={count}" for status, count in sorted(counts.items()))

    def _save_selected_profile(self) -> None:
        if not self.selected_benchmark_ids:
            self.details.setPlainText("Add controls into the profile selection before saving the profile.")
            return
        if not self.current_items:
            self.details.setPlainText("No CIS controls are loaded for the selected benchmark set.")
            return
        selected_items = [
            item for item in self.current_items if item.benchmark_id in set(self.selected_benchmark_ids)
        ]
        if not selected_items:
            self.details.setPlainText("Selected controls could not be resolved.")
            return
        profile = self.controller.save_profile_template(
            name=self.profile_name.text().strip(),
            os_family=selected_items[0].os_family,
            benchmark_ids=[item.benchmark_id for item in selected_items],
            strictness=self.strictness_combo.currentText(),
        )
        message = (
            "\n".join(
                [
                    f"Saved profile: {profile.name}",
                    f"OS: {profile.os_family}",
                    f"Controls: {len(profile.benchmark_ids)}",
                    f"Strictness: {profile.strictness}",
                    "This profile is now available on Dashboard and Run Center.",
                ]
            )
        )
        self.on_refresh()
        self.details.setPlainText(message)


class SettingsPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Settings", "Runtime locations and AI mode used by the local workspace.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.labels: dict[str, QtWidgets.QLabel] = {}
        form = QtWidgets.QFormLayout()
        for key in ("Project root", "Workspace root", "Runtime", "Reports", "Database", "Windows repo", "Linux repo"):
            label = QtWidgets.QLabel()
            label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
            self.labels[key] = label
            form.addRow(key, label)

        self.ai_mode = QtWidgets.QLabel()
        self.capabilities = QtWidgets.QLabel()
        self.capabilities.setWordWrap(True)
        form.addRow("AI mode", self.ai_mode)
        form.addRow("Capabilities", self.capabilities)

        box = QtWidgets.QGroupBox("Runtime Configuration")
        box.setLayout(form)
        self.body.addWidget(box)

    def refresh(self) -> None:
        paths = self.controller.paths
        self.labels["Project root"].setText(str(paths.project_root))
        self.labels["Workspace root"].setText(str(paths.workspace_root))
        self.labels["Runtime"].setText(str(paths.runtime_dir))
        self.labels["Reports"].setText(str(paths.reports_dir))
        self.labels["Database"].setText(str(paths.database_path))
        self.labels["Windows repo"].setText(str(paths.windows_repo))
        self.labels["Linux repo"].setText(str(paths.linux_repo))
        self.ai_mode.setText(self.controller.ai_settings.mode)
        self.capabilities.setText(", ".join(module.name for module in self.controller.list_modules()))
