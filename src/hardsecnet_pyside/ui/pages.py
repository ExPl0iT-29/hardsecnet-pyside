from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from PySide6 import QtCore, QtGui, QtWidgets


def _section(text: str) -> QtWidgets.QLabel:
    label = QtWidgets.QLabel(text)
    label.setObjectName("SectionTitle")
    return label


def _item(value: Any) -> QtWidgets.QTableWidgetItem:
    cell = QtWidgets.QTableWidgetItem("" if value is None else str(value))
    cell.setFlags(cell.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
    return cell


def _style_table(table: QtWidgets.QTableWidget) -> None:
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
    table.verticalHeader().setVisible(False)
    table.horizontalHeader().setStretchLastSection(True)
    table.setShowGrid(False)
    table.setMinimumHeight(150)


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


def _paint_status_column(table: QtWidgets.QTableWidget, column: int) -> None:
    palette = {
        "ready": ("#123a2f", "#8ff0bf"),
        "completed": ("#123a2f", "#8ff0bf"),
        "compliant": ("#123a2f", "#8ff0bf"),
        "dry_run_recorded": ("#123a2f", "#8ff0bf"),
        "review_required": ("#44351a", "#f5d47a"),
        "needs review": ("#44351a", "#f5d47a"),
        "review": ("#44351a", "#f5d47a"),
        "missing": ("#4a2022", "#ff9b9b"),
        "blocked": ("#4a2022", "#ff9b9b"),
        "failed": ("#4a2022", "#ff9b9b"),
        "high": ("#4a2022", "#ff9b9b"),
        "medium": ("#44351a", "#f5d47a"),
        "low": ("#123a2f", "#8ff0bf"),
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
        self.body.setSpacing(14)
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)
        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addLayout(self.body)
        root.addStretch(1)


class MetricCard(QtWidgets.QFrame):
    def __init__(self, label: str, accent: str = "cyan") -> None:
        super().__init__()
        self.setObjectName("MetricCard")
        self.setProperty("accent", accent)
        self.setMinimumSize(150, 96)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)
        self.value = QtWidgets.QLabel("0")
        self.value.setObjectName("MetricValue")
        self.label = QtWidgets.QLabel(label)
        self.label.setObjectName("MetricLabel")
        self.label.setWordWrap(True)
        layout.addWidget(self.value)
        layout.addWidget(self.label)

    def set_value(self, value: Any) -> None:
        self.value.setText(str(value))


class DashboardPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__(
            "Dashboard",
            "Current-device benchmark posture, drift, AI review, and report state.",
        )
        self.controller = controller
        self.on_refresh = on_refresh
        self.cards = {
            "controls": MetricCard("Benchmark controls", "cyan"),
            "runs": MetricCard("Local runs", "green"),
            "review": MetricCard("Review items", "amber"),
            "drift": MetricCard("Drift deltas", "coral"),
            "ai": MetricCard("AI tasks", "violet"),
            "reports": MetricCard("Reports", "blue"),
        }
        card_grid = QtWidgets.QGridLayout()
        card_grid.setSpacing(10)
        for index, card in enumerate(self.cards.values()):
            card_grid.addWidget(card, index // 3, index % 3)

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
        actions.addWidget(run_button)
        actions.addStretch(1)

        self.body.addLayout(card_grid)
        self.body.addWidget(self.device_panel)
        self.body.addLayout(actions)
        self.body.addWidget(_section("Latest Findings"))
        self.body.addWidget(self.latest_table)
        self.body.addWidget(_section("Drift Movement"))
        self.body.addWidget(self.drift_table)
        self.body.addWidget(_section("Review Summary"))
        self.body.addWidget(self.summary)

    def refresh(self) -> None:
        snapshot = self.controller.dashboard_snapshot()
        device = snapshot["device"]
        runs = snapshot["runs"]
        latest_run = runs[0] if runs else None
        findings = snapshot["findings"]
        comparisons = snapshot["comparisons"]
        review_count = sum(1 for item in findings if item.status != "Compliant")

        self.cards["controls"].set_value(len(snapshot["items"]))
        self.cards["runs"].set_value(len(runs))
        self.cards["review"].set_value(review_count)
        self.cards["drift"].set_value(len(comparisons))
        self.cards["ai"].set_value(len(snapshot["ai_tasks"]))
        self.cards["reports"].set_value(len(snapshot["reports"]))

        self.device_label.setText(f"{device.name} | {device.os_family}")
        self.device_detail.setText(
            f"{device.hostname} | AI: {self.controller.ai_settings.mode} | "
            f"{len(snapshot['modules'])} modules | {len(snapshot['profiles'])} local profiles"
        )

        _fill(
            self.latest_table,
            ["Benchmark", "Status", "Severity", "Title"],
            [[item.benchmark_id, item.status, item.severity, item.title] for item in findings[:8]],
        )
        _paint_status_column(self.latest_table, 1)
        _fill(
            self.drift_table,
            ["Benchmark", "Delta", "Before", "After"],
            [
                [delta.benchmark_id, delta.delta_type, delta.before_status, delta.after_status]
                for delta in comparisons[:8]
            ],
        )

        if latest_run is None:
            self.summary.setPlainText("No local run has been recorded yet.")
            return
        report = snapshot["latest_report"]
        self.summary.setPlainText(
            "\n".join(
                [
                    f"Latest run: {latest_run.id}",
                    f"Profile: {latest_run.profile_id}",
                    f"Findings: {len(findings)} total, {review_count} requiring review",
                    f"Report: {report.title if report else 'not generated'}",
                ]
            )
        )

    def _run_profile(self) -> None:
        device = self.controller.get_current_device()
        profiles = self.controller.list_profiles(device.os_family) or self.controller.list_profiles()
        if not profiles:
            return
        self.controller.run_profile(profiles[0].id)
        self.on_refresh()


class HardeningPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__(
            "Hardening",
            "Run a benchmark-aware baseline, review findings, and compare before/after posture.",
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

        run_button = QtWidgets.QPushButton("Run Profile")
        run_button.clicked.connect(self._run_profile)

        header = QtWidgets.QHBoxLayout()
        header.addWidget(QtWidgets.QLabel("Profile"))
        header.addWidget(self.profile_combo, 1)
        header.addWidget(run_button)

        device_group = QtWidgets.QGroupBox("Current Device")
        device_form = QtWidgets.QFormLayout(device_group)
        device_form.addRow("Device", self.device_label)

        self.module_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.run_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.finding_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.run_table.itemSelectionChanged.connect(self._show_run_details)

        self.body.addLayout(header)
        self.body.addWidget(device_group)
        self.body.addWidget(QtWidgets.QLabel("Enabled Modules"))
        self.body.addWidget(self.module_table)
        self.body.addWidget(QtWidgets.QLabel("Recent Runs"))
        self.body.addWidget(self.run_table)
        self.body.addWidget(QtWidgets.QLabel("Latest Findings"))
        self.body.addWidget(self.finding_table)
        self.body.addWidget(QtWidgets.QLabel("Run Details"))
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        device = self.controller.get_current_device()
        self.device_label.setText(f"{device.name} ({device.hostname}) - {device.os_family}")

        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        for profile in self.controller.list_profiles(device.os_family):
            self.profile_combo.addItem(profile.name, profile.id)
        if self.profile_combo.count() == 0:
            for profile in self.controller.list_profiles():
                self.profile_combo.addItem(profile.name, profile.id)
        self.profile_combo.blockSignals(False)

        modules = self.controller.list_modules(device.os_family)
        _fill(
            self.module_table,
            ["ID", "Name", "Description"],
            [[module.id, module.name, module.description] for module in modules],
        )

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
        self._show_run_details()

    def _run_profile(self) -> None:
        profile_id = self.profile_combo.currentData()
        if not profile_id:
            return
        self.controller.run_profile(profile_id)
        self.on_refresh()

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
        super().__init__("AI Advisor", "Review benchmark-aware recommendations and approval state.")
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
        snapshot = self.controller.get_dashboard_snapshot()
        run = snapshot.runs[0] if snapshot.runs else None
        if run is None:
            _fill(self.table, ["Agent", "Subject", "Status", "Provider", "Completed"], [])
            self.details.setPlainText("No run is available yet.")
            return
        tasks = self.controller.list_ai_tasks(run.id)
        _fill(
            self.table,
            ["Agent", "Subject", "Status", "Provider", "Completed"],
            [[task.agent_type, task.subject_id, task.status, task.provider, task.completed_at or ""] for task in tasks],
        )
        self._show_details()

    def _show_details(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            snapshot = self.controller.get_dashboard_snapshot()
            run = snapshot.runs[0] if snapshot.runs else None
            if run is None:
                self.details.setPlainText("No recommendations available.")
                return
            grouped = self.controller.get_ai_recommendations(run.id)
            recommendations = [
                *grouped.get("reasoning", []),
                *grouped.get("remediation", []),
                *grouped.get("approvals", []),
            ]
            self.details.setPlainText(
                "\n\n".join(
                    f"{item.proposed_action}\nApproval: {item.approval_state}\nEvidence: {', '.join(item.evidence_used)}"
                    for item in recommendations[:6]
                )
            )
            return
        self.details.setPlainText(
            "\n".join(
                [
                    f"Agent: {selected[0].text()}",
                    f"Subject: {selected[1].text()}",
                    f"Status: {selected[2].text()}",
                    f"Provider: {selected[3].text()}",
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
        self.table.itemSelectionChanged.connect(self._show_details)
        self.body.addWidget(refresh)
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
        self.details.setPlainText(
            "\n".join(
                [
                    f"Report: {payload['report']['title']}",
                    f"Run: {payload['run']['id']}",
                    f"Findings: {len(payload['findings'])}",
                    f"Comparisons: {len(payload['comparisons'])}",
                    f"Device: {payload['device']['name']}",
                ]
            )
        )


class BenchmarksPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Benchmarks", "Inspect benchmark controls, generated scripts, and guarded dry-run evidence.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.current_documents: list[Any] = []
        self.current_items: list[Any] = []
        self.current_readiness: list[Any] = []
        self.path_edit = QtWidgets.QLineEdit()
        self.documents_table = QtWidgets.QTableWidget()
        self.items_table = QtWidgets.QTableWidget()
        self.readiness_table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)

        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self._browse)
        import_button = QtWidgets.QPushButton("Import Benchmark")
        import_button.clicked.connect(self._import)
        dry_run_button = QtWidgets.QPushButton("Dry Run Selected Script")
        dry_run_button.clicked.connect(self._dry_run_selected_script)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.path_edit, 1)
        row.addWidget(browse)
        row.addWidget(import_button)

        script_actions = QtWidgets.QHBoxLayout()
        script_actions.addWidget(dry_run_button)
        script_actions.addStretch(1)

        self.documents_table.itemSelectionChanged.connect(self._show_items)
        self.items_table.itemSelectionChanged.connect(self._show_item_details)
        self.readiness_table.itemSelectionChanged.connect(self._show_script_details)
        self.body.addLayout(row)
        self.body.addWidget(_section("Benchmark Documents"))
        self.body.addWidget(self.documents_table)
        self.body.addWidget(_section("Benchmark Controls"))
        self.body.addWidget(self.items_table)
        self.body.addWidget(_section("Script Readiness"))
        self.body.addLayout(script_actions)
        self.body.addWidget(self.readiness_table)
        self.body.addWidget(_section("Details"))
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        device = self.controller.get_current_device()
        self.current_documents = self.controller.list_benchmark_documents(device.os_family)
        _fill(
            self.documents_table,
            ["Name", "Version", "OS", "Status", "Source"],
            [[doc.name, doc.version, doc.os_family, doc.status, doc.source_type] for doc in self.current_documents],
        )
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
            ["Benchmark", "Title", "Status", "Confidence"],
            [[item.benchmark_id, item.title, item.status, f"{item.confidence:.2f}"] for item in self.current_items],
        )
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
        self.details.setPlainText(
            f"Document: {document.name}\nVersion: {document.version}\nSource: {document.source_path}\n"
            f"Items: {len(self.current_items)}\nScripts: {self._script_readiness_summary()}"
        )

    def _show_item_details(self) -> None:
        selected = self.items_table.selectedItems()
        if not selected:
            return
        self.details.append(
            "\n\nSelected item:\n"
            f"- Benchmark: {selected[0].text()}\n"
            f"- Title: {selected[1].text()}\n"
            f"- Status: {selected[2].text()}\n"
            f"- Confidence: {selected[3].text()}"
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

    def _selected_readiness(self):
        row = self.readiness_table.currentRow()
        if 0 <= row < len(self.current_readiness):
            return self.current_readiness[row]
        return None

    def _script_readiness_summary(self) -> str:
        if not self.current_readiness:
            return "none"
        counts: dict[str, int] = {}
        for item in self.current_readiness:
            counts[item.status] = counts.get(item.status, 0) + 1
        return ", ".join(f"{status}={count}" for status, count in sorted(counts.items()))


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
