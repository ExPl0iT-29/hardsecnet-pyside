from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from PySide6 import QtCore, QtWidgets


def _item(value: Any) -> QtWidgets.QTableWidgetItem:
    cell = QtWidgets.QTableWidgetItem("" if value is None else str(value))
    cell.setFlags(cell.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
    return cell


def _fill(table: QtWidgets.QTableWidget, headers: list[str], rows: list[list[Any]]) -> None:
    table.clear()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(rows))
    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            table.setItem(row_index, column_index, _item(value))
    table.resizeColumnsToContents()


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
        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addLayout(self.body)
        root.addStretch(1)


class FleetDashboardPage(BasePage):
    def __init__(self, controller, on_refresh: Callable[[], None]) -> None:
        super().__init__("Fleet", "Track enrolled devices, heartbeats, jobs, and campaigns.")
        self.controller = controller
        self.on_refresh = on_refresh

        self.device_id_edit = QtWidgets.QLineEdit("fleet-demo-01")
        self.device_name_edit = QtWidgets.QLineEdit("Fleet Demo Device")
        self.device_host_edit = QtWidgets.QLineEdit("fleet-demo-host")
        self.device_os_combo = QtWidgets.QComboBox()
        self.device_os_combo.addItems(["windows", "linux"])
        self.device_caps_edit = QtWidgets.QLineEdit("audit,compare,report-sync")
        self.job_action_edit = QtWidgets.QLineEdit("remote-audit")
        self.job_payload_edit = QtWidgets.QPlainTextEdit()
        self.job_payload_edit.setPlainText(json.dumps({"campaign": "baseline", "benchmark_scope": []}, indent=2))
        self.job_summary_edit = QtWidgets.QLineEdit("Remote job completed successfully.")

        enroll_button = QtWidgets.QPushButton("Enroll Device")
        enroll_button.clicked.connect(self._enroll_device)
        heartbeat_button = QtWidgets.QPushButton("Heartbeat Selected")
        heartbeat_button.clicked.connect(self._record_heartbeat)
        queue_button = QtWidgets.QPushButton("Queue Job")
        queue_button.clicked.connect(self._queue_job)
        claim_button = QtWidgets.QPushButton("Claim Job")
        claim_button.clicked.connect(self._claim_job)
        complete_button = QtWidgets.QPushButton("Complete Job")
        complete_button.clicked.connect(self._complete_job)
        campaign_button = QtWidgets.QPushButton("Create Campaign")
        campaign_button.clicked.connect(self._create_campaign)
        refresh_button = QtWidgets.QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)

        form = QtWidgets.QFormLayout()
        form.addRow("Device ID", self.device_id_edit)
        form.addRow("Device Name", self.device_name_edit)
        form.addRow("Hostname", self.device_host_edit)
        form.addRow("OS Family", self.device_os_combo)
        form.addRow("Capabilities", self.device_caps_edit)
        form.addRow("Job Action", self.job_action_edit)
        form.addRow("Job Payload", self.job_payload_edit)
        form.addRow("Job Summary", self.job_summary_edit)

        button_row = QtWidgets.QHBoxLayout()
        for button in (enroll_button, heartbeat_button, queue_button, claim_button, complete_button, campaign_button, refresh_button):
            button_row.addWidget(button)

        self.device_table = QtWidgets.QTableWidget()
        self.job_table = QtWidgets.QTableWidget()
        self.result_table = QtWidgets.QTableWidget()
        self.campaign_table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)

        self.device_table.itemSelectionChanged.connect(self._show_details)
        self.job_table.itemSelectionChanged.connect(self._show_details)
        self.result_table.itemSelectionChanged.connect(self._show_details)

        self.body.addLayout(form)
        self.body.addLayout(button_row)
        self.body.addWidget(QtWidgets.QLabel("Devices"))
        self.body.addWidget(self.device_table)
        self.body.addWidget(QtWidgets.QLabel("Jobs"))
        self.body.addWidget(self.job_table)
        self.body.addWidget(QtWidgets.QLabel("Results"))
        self.body.addWidget(self.result_table)
        self.body.addWidget(QtWidgets.QLabel("Campaigns"))
        self.body.addWidget(self.campaign_table)
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        snapshot = self.controller.fleet_snapshot()
        _fill(
            self.device_table,
            ["Device ID", "Name", "OS", "Hostname", "Heartbeat", "Queued", "Capabilities"],
            [
                [
                    row.device.id,
                    row.device.name,
                    row.device.os_family,
                    row.device.hostname,
                    row.heartbeat_status,
                    row.queued_jobs,
                    ", ".join(row.manifest.capabilities) if row.manifest else "",
                ]
                for row in snapshot.devices
            ],
        )
        _fill(
            self.job_table,
            ["Job ID", "Device", "Action", "Status", "Approval", "Claimed", "Completed", "Summary"],
            [
                [
                    row.job.id,
                    row.job.device_id,
                    row.job.action,
                    row.status,
                    "yes" if row.job.approval_required else "no",
                    row.claimed_at,
                    row.completed_at,
                    row.summary,
                ]
                for row in snapshot.jobs
            ],
        )
        _fill(
            self.result_table,
            ["Job", "Device", "Status", "Summary", "Artifacts"],
            [
                [
                    result.job_id,
                    result.device_id,
                    result.status,
                    result.summary,
                    ", ".join(result.artifacts),
                ]
                for result in snapshot.results
            ],
        )
        _fill(
            self.campaign_table,
            ["Campaign", "Name", "Devices", "Benchmarks", "Created"],
            [
                [
                    campaign.id,
                    campaign.name,
                    ", ".join(campaign.device_ids),
                    ", ".join(campaign.benchmark_scope),
                    campaign.created_at,
                ]
                for campaign in snapshot.campaigns
            ],
        )
        self._show_details()

    def _selected_device_id(self) -> str:
        selected = self.device_table.selectedItems()
        if selected:
            return selected[0].text()
        if self.device_table.rowCount():
            return self.device_table.item(0, 0).text()
        return self.controller.get_current_device().id

    def _selected_job_id(self) -> str | None:
        selected = self.job_table.selectedItems()
        if selected:
            return selected[0].text()
        if self.job_table.rowCount():
            return self.job_table.item(0, 0).text()
        return None

    def _enroll_device(self) -> None:
        caps = [item.strip() for item in self.device_caps_edit.text().split(",") if item.strip()]
        self.controller.enroll_fleet_device(
            device_id=self.device_id_edit.text().strip(),
            name=self.device_name_edit.text().strip(),
            os_family=self.device_os_combo.currentText(),
            hostname=self.device_host_edit.text().strip(),
            capabilities=caps,
            metadata={"source": "ui-demo"},
        )
        self.controller.record_fleet_heartbeat(self.device_id_edit.text().strip(), "healthy", 0)
        self.on_refresh()

    def _record_heartbeat(self) -> None:
        device_id = self._selected_device_id()
        queued = self.controller.fleet_snapshot().queued_job_count
        self.controller.record_fleet_heartbeat(device_id, "healthy", queued)
        self.on_refresh()

    def _queue_job(self) -> None:
        device_id = self._selected_device_id()
        try:
            payload = json.loads(self.job_payload_edit.toPlainText() or "{}")
        except json.JSONDecodeError:
            payload = {"raw": self.job_payload_edit.toPlainText()}
        self.controller.queue_fleet_job(
            device_id=device_id,
            action=self.job_action_edit.text().strip() or "remote-audit",
            payload=payload,
            approval_required=True,
        )
        self.on_refresh()

    def _claim_job(self) -> None:
        job_id = self._selected_job_id()
        if not job_id:
            self.details.setPlainText("No fleet job is available to claim.")
            return
        self.controller.claim_fleet_job(job_id)
        self.on_refresh()

    def _complete_job(self) -> None:
        job_id = self._selected_job_id()
        if not job_id:
            self.details.setPlainText("No fleet job is available to complete.")
            return
        self.controller.complete_fleet_job(
            job_id,
            summary=self.job_summary_edit.text().strip() or "Remote job completed successfully.",
            artifacts=[str(self.controller.paths.artifacts_dir / f"{job_id}.json")],
        )
        self.on_refresh()

    def _create_campaign(self) -> None:
        snapshot = self.controller.fleet_snapshot()
        device_ids = [row.device.id for row in snapshot.devices] or [self.controller.get_current_device().id]
        self.controller.create_fleet_campaign(
            name="Fleet Baseline Campaign",
            device_ids=device_ids,
            benchmark_scope=["CIS baseline", "fleet compare"],
        )
        self.on_refresh()

    def _show_details(self) -> None:
        snapshot = self.controller.fleet_snapshot()
        if not snapshot.devices:
            self.details.setPlainText("No enrolled devices yet.")
            return
        device_id = self._selected_device_id()
        job_id = self._selected_job_id()
        device = next((row for row in snapshot.devices if row.device.id == device_id), snapshot.devices[0])
        job = next((row for row in snapshot.jobs if row.job.id == job_id), None)
        lines = [
            f"Device: {device.device.name} ({device.device.id})",
            f"Heartbeat: {device.heartbeat_status}",
            f"Queued jobs: {device.queued_jobs}",
        ]
        if job is not None:
            lines.extend(
                [
                    "",
                    f"Selected job: {job.job.id}",
                    f"Action: {job.job.action}",
                    f"Status: {job.status}",
                    f"Summary: {job.summary or 'not completed'}",
                ]
            )
        self.details.setPlainText("\n".join(lines))


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
        super().__init__("Benchmarks", "Inspect seeded benchmark data and import imported controls.")
        self.controller = controller
        self.on_refresh = on_refresh
        self.path_edit = QtWidgets.QLineEdit()
        self.documents_table = QtWidgets.QTableWidget()
        self.items_table = QtWidgets.QTableWidget()
        self.details = QtWidgets.QTextEdit()
        self.details.setReadOnly(True)

        browse = QtWidgets.QPushButton("Browse")
        browse.clicked.connect(self._browse)
        import_button = QtWidgets.QPushButton("Import Benchmark")
        import_button.clicked.connect(self._import)

        row = QtWidgets.QHBoxLayout()
        row.addWidget(self.path_edit, 1)
        row.addWidget(browse)
        row.addWidget(import_button)

        self.documents_table.itemSelectionChanged.connect(self._show_items)
        self.items_table.itemSelectionChanged.connect(self._show_item_details)
        self.body.addLayout(row)
        self.body.addWidget(self.documents_table)
        self.body.addWidget(self.items_table)
        self.body.addWidget(self.details)

    def refresh(self) -> None:
        device = self.controller.get_current_device()
        documents = self.controller.list_benchmark_documents(device.os_family)
        _fill(
            self.documents_table,
            ["Name", "Version", "OS", "Status", "Source"],
            [[doc.name, doc.version, doc.os_family, doc.status, doc.source_type] for doc in documents],
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
        docs = self.controller.list_benchmark_documents(device.os_family)
        if not docs:
            _fill(self.items_table, ["Benchmark", "Title", "Status", "Confidence"], [])
            self.details.setPlainText("No benchmark documents are available.")
            return
        row = self.documents_table.currentRow()
        document = docs[min(max(row, 0), len(docs) - 1)]
        items = self.controller.list_benchmark_items(document.id)
        _fill(
            self.items_table,
            ["Benchmark", "Title", "Status", "Confidence"],
            [[item.benchmark_id, item.title, item.status, f"{item.confidence:.2f}"] for item in items],
        )
        self.details.setPlainText(
            f"Document: {document.name}\nVersion: {document.version}\nSource: {document.source_path}\nItems: {len(items)}"
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
