from __future__ import annotations

import hashlib
import json
import re
import uuid
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path

from hardsecnet_pyside.models import (
    BenchmarkDocument,
    BenchmarkItem,
    CheckLogic,
    EvidenceField,
    RemediationStep,
)


CONTROL_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+(.*\S)\s*$")
CIS_CONTROL_LINE = re.compile(
    r"^(?P<id>\d+(?:\.\d+)+)\s+"
    r"(?:(?P<level>\((?:L1|L2)(?:\s*NG)?\))\s+)?"
    r"(?P<title>.+?)"
    r"(?:\s+\((?P<automation>Automated|Manual)\))?\s*$",
    re.MULTILINE,
)
SECTION_LABELS = [
    "Profile Applicability",
    "Description",
    "Rationale",
    "Impact",
    "Audit",
    "Remediation",
    "Default Value",
    "References",
    "Additional Information",
]
SECTION_HEADER = re.compile(
    r"^(?P<label>" + "|".join(re.escape(item) for item in SECTION_LABELS) + r"):\s*$",
    re.MULTILINE,
)
BULLET_CHARS = {"•": "-", "●": "-", "▪": "-", "◦": "-"}


@dataclass(slots=True)
class ParsedControl:
    benchmark_id: str
    title: str
    profile_level: str
    automated: bool
    source_page: int | None
    body: str
    sections: dict[str, str]


class BenchmarkImportError(RuntimeError):
    """Raised when benchmark import fails."""


class BenchmarkImporter:
    def import_path(self, path: Path) -> tuple[BenchmarkDocument, list[BenchmarkItem]]:
        suffix = path.suffix.lower()
        if suffix in {".xml", ".xccdf", ".oval"}:
            return self._import_xml(path)
        if suffix == ".json":
            return self._import_json(path)
        if suffix == ".pdf":
            return self._import_pdf(path)
        return self._import_text(path)

    def generate_script_candidates(self, document: BenchmarkDocument, items: list[BenchmarkItem], output_dir: Path) -> list[str]:
        output_dir.mkdir(parents=True, exist_ok=True)
        extension = ".ps1" if document.os_family == "windows" else ".sh"
        paths: list[str] = []
        for item in items:
            script_path = output_dir / f"{self._slug(item.benchmark_id)}{extension}"
            script_path.write_text(self._render_script_candidate(document, item), encoding="utf-8")
            paths.append(str(script_path))
        return paths


    def export_benchmark_bundle(self, document: BenchmarkDocument, items: list[BenchmarkItem], output_root: Path) -> dict[str, str | int]:
        bundle_dir = output_root / self._slug(f"{document.name}-{document.version}")
        scripts_dir = bundle_dir / "scripts"
        bundle_dir.mkdir(parents=True, exist_ok=True)
        document_path = bundle_dir / "benchmark_document.json"
        items_path = bundle_dir / "benchmark_items.json"
        index_path = bundle_dir / "README.md"
        document_path.write_text(json.dumps(asdict(document), indent=2, sort_keys=True), encoding="utf-8")
        items_path.write_text(json.dumps([asdict(item) for item in items], indent=2, sort_keys=True), encoding="utf-8")
        generated_paths = self.generate_script_candidates(document, items, scripts_dir)
        index_path.write_text(self._render_bundle_readme(document, items, generated_paths), encoding="utf-8")
        return {
            'bundle_dir': str(bundle_dir),
            'document_path': str(document_path),
            'items_path': str(items_path),
            'scripts_dir': str(scripts_dir),
            'script_count': len(generated_paths),
            'readme_path': str(index_path),
        }

    def _document_hash(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _make_document(
        self, *, path: Path, name: str, version: str, os_family: str, source_type: str, status: str
    ) -> BenchmarkDocument:
        return BenchmarkDocument(
            id=f"doc-{uuid.uuid4().hex[:12]}",
            name=name,
            version=version,
            os_family=os_family,
            source_type=source_type,
            source_path=str(path),
            source_hash=self._document_hash(path),
            status=status,
            provenance={"filename": path.name},
        )

    def _import_xml(self, path: Path) -> tuple[BenchmarkDocument, list[BenchmarkItem]]:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        ns = {"xccdf": "http://checklists.nist.gov/xccdf/1.2"}

        benchmark_id = root.attrib.get("id", path.stem)
        title = root.findtext(".//xccdf:title", default=path.stem, namespaces=ns)
        version = root.findtext(".//xccdf:version", default="imported", namespaces=ns)
        description = root.findtext(".//xccdf:description", default="", namespaces=ns)
        os_family = "windows" if "windows" in title.lower() else "linux"

        document = self._make_document(
            path=path,
            name=title,
            version=version,
            os_family=os_family,
            source_type="machine-readable",
            status="review_required",
        )
        document.provenance.update({"benchmark_id": benchmark_id, "description": description[:500]})

        items: list[BenchmarkItem] = []
        for index, rule in enumerate(root.findall(".//xccdf:Rule", ns), start=1):
            rule_id = rule.attrib.get("id", f"{benchmark_id}-rule-{index}")
            rule_title = rule.findtext("xccdf:title", default=rule_id, namespaces=ns)
            rationale = rule.findtext("xccdf:rationale", default="", namespaces=ns)
            fixtext = rule.findtext("xccdf:fixtext", default="", namespaces=ns)
            automated = bool(rule.findall("xccdf:check", ns))
            items.append(
                BenchmarkItem(
                    id=f"item-{uuid.uuid4().hex[:12]}",
                    document_id=document.id,
                    benchmark_id=rule_id,
                    title=rule_title,
                    os_family=os_family,
                    profile_level="L1",
                    automated=automated,
                    rationale=rationale,
                    recommendation=fixtext or rule_title,
                    audit_logic=[
                        CheckLogic(
                            kind="imported_rule",
                            target=rule_id,
                            operator="manual_review",
                            expected="See imported rule check content",
                            notes="Imported from machine-readable benchmark content.",
                        )
                    ],
                    remediation_steps=[
                        RemediationStep(
                            title="Imported remediation guidance",
                            command=fixtext or "Manual review required",
                            expected_impact="Align device closer to imported benchmark guidance.",
                            rollback="Review remediation manually before execution.",
                            approval_required=True,
                        )
                    ],
                    rollback_notes=["Imported items require review before becoming runnable."],
                    evidence_fields=[
                        EvidenceField(
                            name="imported_evidence",
                            description="Evidence required by imported machine-readable benchmark.",
                            required=True,
                        )
                    ],
                    citations=[rule_id],
                    confidence=0.92 if automated else 0.78,
                    status="review_required",
                    candidate_modules=self._suggest_modules(rule_title),
                )
            )
        return document, items

    def _import_json(self, path: Path) -> tuple[BenchmarkDocument, list[BenchmarkItem]]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        document = self._make_document(
            path=path,
            name=payload.get("name", path.stem),
            version=payload.get("version", "imported"),
            os_family=payload.get("os_family", "linux"),
            source_type="structured-json",
            status="review_required",
        )
        items: list[BenchmarkItem] = []
        for entry in payload.get("items", []):
            items.append(
                BenchmarkItem(
                    id=f"item-{uuid.uuid4().hex[:12]}",
                    document_id=document.id,
                    benchmark_id=entry["benchmark_id"],
                    title=entry["title"],
                    os_family=entry.get("os_family", document.os_family),
                    profile_level=entry.get("profile_level", "L1"),
                    automated=entry.get("automated", False),
                    rationale=entry.get("rationale", ""),
                    recommendation=entry.get("recommendation", ""),
                    audit_logic=[CheckLogic(**logic) for logic in entry.get("audit_logic", [])],
                    remediation_steps=[
                        RemediationStep(**step) for step in entry.get("remediation_steps", [])
                    ],
                    rollback_notes=entry.get("rollback_notes", []),
                    evidence_fields=[EvidenceField(**field) for field in entry.get("evidence_fields", [])],
                    citations=entry.get("citations", []),
                    confidence=float(entry.get("confidence", 0.8)),
                    status=entry.get("status", "review_required"),
                    candidate_modules=entry.get(
                        "candidate_modules", self._suggest_modules(entry.get("title", ""))
                    ),
                )
            )
        return document, items

    def _import_pdf(self, path: Path) -> tuple[BenchmarkDocument, list[BenchmarkItem]]:
        try:
            import fitz  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise BenchmarkImportError(
                "PDF import requires PyMuPDF. Install the project dependencies first."
            ) from exc

        with fitz.open(path) as document_handle:
            pages = [self._normalize_pdf_text(page.get_text("text")) for page in document_handle]
        text = "\n".join(pages).strip()
        if not text:
            raise BenchmarkImportError("PDF text extraction returned no content.")

        header = pages[0] if pages else path.stem
        name = self._extract_name(header, path)
        version = self._extract_version(header, path)
        os_family = "windows" if "windows" in name.lower() or "windows" in path.stem.lower() else "linux"
        document = self._make_document(
            path=path,
            name=name,
            version=version,
            os_family=os_family,
            source_type="pdf-text",
            status="review_required",
        )
        document.provenance["page_count"] = len(pages)
        parsed_controls = self._parse_cis_pdf_controls(pages)
        items = [self._parsed_control_to_item(document, control) for control in parsed_controls]
        return document, items

    def _import_text(self, path: Path) -> tuple[BenchmarkDocument, list[BenchmarkItem]]:
        document = self._make_document(
            path=path,
            name=path.stem,
            version="text-import",
            os_family="windows" if "windows" in path.stem.lower() else "linux",
            source_type="text",
            status="review_required",
        )
        return document, self._parse_controls_from_text(
            document, path.read_text(encoding="utf-8", errors="ignore"), 0.72
        )

    def _parse_cis_pdf_controls(self, pages: list[str]) -> list[ParsedControl]:
        joined = []
        page_for_offset: list[tuple[int, int]] = []
        offset = 0
        for idx, page in enumerate(pages, start=1):
            marker = f"\n[[[PAGE:{idx}]]]\n"
            chunk = marker + page + "\n"
            joined.append(chunk)
            page_for_offset.append((offset, idx))
            offset += len(chunk)
        text = "".join(joined)

        matches = list(CIS_CONTROL_LINE.finditer(text))
        controls: list[ParsedControl] = []
        for index, match in enumerate(matches):
            benchmark_id = match.group("id")
            if benchmark_id.count(".") < 2:
                continue
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = text[match.end():end].strip()
            if not self._looks_like_control_body(body):
                continue
            cleaned_body = self._strip_page_markers(body)
            title, automated = self._finalize_control_header(
                self._clean_inline(match.group("title")),
                cleaned_body,
                (match.group("automation") or "").lower() == "automated",
            )
            sections = self._split_sections(cleaned_body)
            source_page = self._page_for_offset(text[:start])
            controls.append(
                ParsedControl(
                    benchmark_id=benchmark_id,
                    title=title,
                    profile_level=(match.group("level") or "L1").strip("()"),
                    automated=automated,
                    source_page=source_page,
                    body=cleaned_body,
                    sections=sections,
                )
            )
        if not controls:
            raise BenchmarkImportError("No CIS benchmark controls were detected in the imported PDF.")
        return controls

    def _page_for_offset(self, prefix_text: str) -> int | None:
        matches = re.findall(r"\[\[\[PAGE:(\d+)\]\]\]", prefix_text)
        return int(matches[-1]) if matches else None

    def _looks_like_control_body(self, body: str) -> bool:
        trimmed = self._strip_page_markers(body)
        if len(trimmed) < 80:
            return False
        required_signals = (
            "Description:",
            "Audit:",
            "Remediation:",
            "Rationale:",
            "Profile Applicability:",
        )
        return any(signal in trimmed for signal in required_signals)

    def _split_sections(self, body: str) -> dict[str, str]:
        cleaned = self._strip_page_markers(body)
        matches = list(SECTION_HEADER.finditer(cleaned))
        if not matches:
            return {"Description": cleaned.strip()}
        sections: dict[str, str] = {}
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(cleaned)
            sections[match.group("label")] = cleaned[start:end].strip()
        return sections


    def _finalize_control_header(self, initial_title: str, cleaned_body: str, automated: bool) -> tuple[str, bool]:
        section_match = SECTION_HEADER.search(cleaned_body)
        preamble = cleaned_body[:section_match.start()].strip() if section_match else ""
        title = self._clean_inline(f"{initial_title} {preamble}") if preamble else initial_title
        if title.endswith("(Automated)"):
            automated = True
            title = title[: -len("(Automated)")].strip()
        elif title.endswith("(Manual)"):
            automated = False
            title = title[: -len("(Manual)")].strip()
        return title, automated

    def _parsed_control_to_item(self, document: BenchmarkDocument, control: ParsedControl) -> BenchmarkItem:
        recommendation = self._recommendation_from_sections(control)
        audit_text = control.sections.get("Audit", "Manual review of the imported benchmark control is required.")
        citations = [control.benchmark_id]
        if control.source_page is not None:
            citations.append(f"page:{control.source_page}")
        return BenchmarkItem(
            id=f"item-{uuid.uuid4().hex[:12]}",
            document_id=document.id,
            benchmark_id=control.benchmark_id,
            title=control.title,
            os_family=document.os_family,
            profile_level=control.profile_level,
            automated=control.automated,
            rationale=control.sections.get("Rationale", control.sections.get("Description", ""))[:4000],
            recommendation=recommendation,
            audit_logic=self._build_audit_logic(control),
            remediation_steps=self._build_remediation_steps(control),
            rollback_notes=self._build_rollback_notes(control),
            evidence_fields=self._build_evidence_fields(control),
            source_page=control.source_page,
            citations=citations,
            confidence=self._confidence_for_control(control),
            status="review_required",
            tags=self._tags_for_control(control),
            candidate_modules=self._suggest_modules(control.title),
        )

    def _build_audit_logic(self, control: ParsedControl) -> list[CheckLogic]:
        audit = self._clean_block(control.sections.get("Audit", ""))
        if not audit:
            audit = "Manual audit procedure not extracted cleanly. Review benchmark text."
        kind = "cis_audit_procedure" if control.automated else "cis_manual_procedure"
        operator = "review_required"
        target = control.benchmark_id
        if control.os_family if hasattr(control, 'os_family') else False:
            pass
        return [
            CheckLogic(
                kind=kind,
                target=target,
                operator=operator,
                expected=control.title,
                notes=audit[:1500],
            )
        ]

    def _build_remediation_steps(self, control: ParsedControl) -> list[RemediationStep]:
        remediation = self._clean_block(control.sections.get("Remediation", ""))
        if not remediation:
            remediation = "No remediation text extracted. Manual mapping required."
        commands = self._extract_command_lines(remediation)
        if commands:
            command = "\n".join(commands[:20])
        elif "Navigate to the UI Path" in remediation or "set to" in remediation:
            command = "# Manual policy mapping required\n# Review the remediation text and map to a registry/GPO/script action"
        else:
            command = "# Manual review required\n# Convert the remediation guidance below into a validated script action"
        return [
            RemediationStep(
                title=f"Remediate {control.benchmark_id}",
                command=command,
                expected_impact=self._clean_inline(control.sections.get("Impact", "Align to benchmark guidance."))[:500],
                rollback="Review the benchmark text and create a tested rollback before production use.",
                approval_required=True,
            )
        ]

    def _build_rollback_notes(self, control: ParsedControl) -> list[str]:
        notes = [
            "Generated from CIS PDF extraction. Validate before execution.",
            "Create rollback steps after confirming the remediation mapping on a test host.",
        ]
        default_value = self._clean_block(control.sections.get("Default Value", ""))
        if default_value:
            notes.append(f"Default Value: {default_value[:500]}")
        return notes

    def _build_evidence_fields(self, control: ParsedControl) -> list[EvidenceField]:
        fields = [
            EvidenceField(
                name="audit_procedure_output",
                description="Output captured while following the imported CIS audit procedure.",
                required=True,
            )
        ]
        if control.sections.get("Remediation"):
            fields.append(
                EvidenceField(
                    name="remediation_validation",
                    description="Post-remediation validation showing the prescribed state was achieved.",
                    required=True,
                )
            )
        return fields

    def _confidence_for_control(self, control: ParsedControl) -> float:
        score = 0.78
        if control.automated:
            score += 0.08
        if control.sections.get("Audit"):
            score += 0.05
        if control.sections.get("Remediation"):
            score += 0.05
        if control.source_page is not None:
            score += 0.02
        return min(score, 0.96)

    def _tags_for_control(self, control: ParsedControl) -> list[str]:
        tags = [control.profile_level.lower(), "automated" if control.automated else "manual"]
        lowered = control.title.lower()
        for token in ("firewall", "network", "password", "audit", "ssh", "defender", "kernel", "cron"):
            if token in lowered:
                tags.append(token)
        return sorted(set(tags))

    def _recommendation_from_sections(self, control: ParsedControl) -> str:
        remediation = self._clean_inline(control.sections.get("Remediation", ""))
        if remediation:
            return remediation[:1000]
        description = self._clean_inline(control.sections.get("Description", ""))
        return description[:1000] if description else control.title

    def _parse_controls_from_text(
        self, document: BenchmarkDocument, text: str, base_confidence: float
    ) -> list[BenchmarkItem]:
        items: list[BenchmarkItem] = []
        current_id = ""
        current_title = ""
        body: list[str] = []

        def flush() -> None:
            nonlocal current_id, current_title, body
            if not current_id:
                return
            description = "\n".join(line for line in body if line.strip()).strip()
            items.append(
                BenchmarkItem(
                    id=f"item-{uuid.uuid4().hex[:12]}",
                    document_id=document.id,
                    benchmark_id=current_id,
                    title=current_title,
                    os_family=document.os_family,
                    profile_level="L1",
                    automated=False,
                    rationale=description[:800],
                    recommendation=current_title,
                    audit_logic=[
                        CheckLogic(
                            kind="manual_text_import",
                            target=current_id,
                            operator="review_required",
                            expected="Human review of imported benchmark text",
                            notes=description[:400],
                        )
                    ],
                    remediation_steps=[
                        RemediationStep(
                            title="Review imported recommendation",
                            command="Manual review required",
                            expected_impact="Use imported benchmark item to build curated profile and mappings.",
                            rollback="No automated rollback available until mapped.",
                            approval_required=True,
                        )
                    ],
                    rollback_notes=["Imported from unstructured text or PDF. Review before execution."],
                    evidence_fields=[
                        EvidenceField(
                            name="manual_evidence",
                            description="Evidence to be defined during control mapping review.",
                            required=True,
                        )
                    ],
                    citations=[current_id],
                    confidence=base_confidence,
                    status="review_required",
                    candidate_modules=self._suggest_modules(current_title),
                )
            )
            current_id = ""
            current_title = ""
            body = []

        for raw_line in text.splitlines():
            line = raw_line.strip()
            match = CONTROL_PATTERN.match(line)
            if match:
                flush()
                current_id = match.group(1)
                current_title = match.group(2)
            elif current_id:
                body.append(line)
        flush()
        if not items:
            raise BenchmarkImportError("No benchmark controls were detected in the imported document.")
        return items

    def _suggest_modules(self, title: str) -> list[str]:
        lowered = title.lower()
        modules = {"cis_audit"}
        if any(token in lowered for token in ("firewall", "password", "lock", "ssh", "uac", "rdp", "kernel", "defender", "systemd", "chrony", "cron", "network")):
            modules.add("baseline_harden")
        if any(token in lowered for token in ("drift", "compare", "difference", "audit")):
            modules.add("drift_check")
        if any(token in lowered for token in ("snapshot", "backup", "rollback")):
            modules.add("baseline_snapshot")
        if len(modules) == 1:
            modules.update({"baseline_harden", "drift_check"})
        return sorted(modules)

    def _normalize_pdf_text(self, text: str) -> str:
        normalized = text.replace("\r", "")
        for src, dst in BULLET_CHARS.items():
            normalized = normalized.replace(src, dst)
        return normalized

    def _strip_page_markers(self, text: str) -> str:
        return re.sub(r"\n?\[\[\[PAGE:\d+\]\]\]\n?", "\n", text).strip()

    def _extract_name(self, header: str, path: Path) -> str:
        cleaned = self._strip_page_markers(header)
        lines = [self._clean_inline(line) for line in cleaned.splitlines() if self._clean_inline(line)]
        title_lines = [line for line in lines if not re.search(r"v\d+\.\d+\.\d+|\d{2}[-/]\d{2}[-/]\d{4}", line, re.IGNORECASE)]
        return " ".join(title_lines[:4]) or path.stem

    def _extract_version(self, header: str, path: Path) -> str:
        cleaned = self._strip_page_markers(header)
        match = re.search(r"v\d+(?:\.\d+)+", cleaned, re.IGNORECASE)
        return match.group(0) if match else path.stem

    def _extract_command_lines(self, remediation: str) -> list[str]:
        lines = [self._clean_inline(line) for line in remediation.splitlines() if self._clean_inline(line)]
        commands: list[str] = []
        for line in lines:
            if any(token in line for token in ("/etc/", "systemctl", "modprobe", "ufw ", "sshd", "auditctl", "pwquality", "registry", "Set-", "New-Item", "Set-ItemProperty", "reg add", "secedit", "net accounts")):
                commands.append(line)
            elif line.startswith("-") and len(line) > 2:
                commands.append(f"# {line[1:].strip()}")
        return commands

    def _render_script_candidate(self, document: BenchmarkDocument, item: BenchmarkItem) -> str:
        if document.os_family == "windows":
            return self._render_powershell_candidate(document, item)
        return self._render_bash_candidate(document, item)


    def _render_bundle_readme(self, document: BenchmarkDocument, items: list[BenchmarkItem], generated_paths: list[str]) -> str:
        lines = [
            f"# {document.name}",
            "",
            f"- Version: `{document.version}`",
            f"- OS Family: `{document.os_family}`",
            f"- Source Type: `{document.source_type}`",
            f"- Source Hash: `{document.source_hash}`",
            f"- Imported At: `{document.imported_at}`",
            f"- Control Count: `{len(items)}`",
            f"- Script Count: `{len(generated_paths)}`",
            "",
            "## Files",
            "",
            "- `benchmark_document.json`: normalized document metadata",
            "- `benchmark_items.json`: extracted controls with remediation and audit data",
            "- `scripts/`: generated script candidates, one file per control",
            "",
            "## First Controls",
            "",
        ]
        for item in items[:10]:
            lines.append(f"- `{item.benchmark_id}` {item.title}")
        return "\n".join(lines) + "\n"

    def _render_powershell_candidate(self, document: BenchmarkDocument, item: BenchmarkItem) -> str:
        remediation = item.remediation_steps[0].command if item.remediation_steps else "# Manual review required"
        audit_notes = item.audit_logic[0].notes if item.audit_logic else "Manual review required"
        lines = [
            f"# CIS Benchmark: {document.name}",
            f"# Control: {item.benchmark_id} - {item.title}",
            f"# Source Page: {item.source_page or 'unknown'}",
            f"# Confidence: {item.confidence}",
            f"# Status: {item.status}",
            "",
            "$ErrorActionPreference = 'Stop'",
            "",
            "# Audit guidance extracted from the benchmark",
        ]
        lines.extend(f"# {line}" for line in audit_notes.splitlines() if line.strip())
        lines.extend([
            "",
            "# Remediation candidate",
        ])
        lines.extend(remediation.splitlines() or ["# Manual mapping required"])
        lines.extend([
            "",
            "# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.",
        ])
        return "\n".join(lines) + "\n"

    def _render_bash_candidate(self, document: BenchmarkDocument, item: BenchmarkItem) -> str:
        remediation = item.remediation_steps[0].command if item.remediation_steps else "# Manual review required"
        audit_notes = item.audit_logic[0].notes if item.audit_logic else "Manual review required"
        lines = [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            f"# CIS Benchmark: {document.name}",
            f"# Control: {item.benchmark_id} - {item.title}",
            f"# Source Page: {item.source_page or 'unknown'}",
            f"# Confidence: {item.confidence}",
            f"# Status: {item.status}",
            "",
            "# Audit guidance extracted from the benchmark",
        ]
        lines.extend(f"# {line}" for line in audit_notes.splitlines() if line.strip())
        lines.extend([
            "",
            "# Remediation candidate",
        ])
        lines.extend(remediation.splitlines() or ["# Manual mapping required"])
        lines.extend([
            "",
            "# TODO: replace the commented/manual steps above with validated bash remediation logic.",
        ])
        return "\n".join(lines) + "\n"

    def _slug(self, value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-").lower()

    def _clean_inline(self, text: str) -> str:
        return re.sub(r"\s+", " ", text or "").strip()

    def _clean_block(self, text: str) -> str:
        lines = [self._clean_inline(line) for line in (text or "").splitlines()]
        return "\n".join(line for line in lines if line)
