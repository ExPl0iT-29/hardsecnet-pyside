from __future__ import annotations

import hashlib
import json
import re
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from hardsecnet_pyside.models import (
    BenchmarkDocument,
    BenchmarkItem,
    CheckLogic,
    EvidenceField,
    RemediationStep,
)


CONTROL_PATTERN = re.compile(r"^\s*(\d+(?:\.\d+)+)\s+(.*\S)\s*$")


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
            pages = [page.get_text("text") for page in document_handle]
        text = "\n".join(pages).strip()
        if not text:
            raise BenchmarkImportError("PDF text extraction returned no content.")
        document = self._make_document(
            path=path,
            name=path.stem,
            version="pdf-import",
            os_family="windows" if "windows" in path.stem.lower() else "linux",
            source_type="pdf-text",
            status="review_required",
        )
        document.provenance["page_count"] = len(pages)
        return document, self._parse_controls_from_text(document, text, 0.66)

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
        if any(token in lowered for token in ("firewall", "password", "lock", "ssh", "uac", "rdp")):
            modules.add("baseline_harden")
        if any(token in lowered for token in ("drift", "compare", "difference")):
            modules.add("drift_check")
        if any(token in lowered for token in ("snapshot", "backup", "rollback")):
            modules.add("baseline_snapshot")
        if len(modules) == 1:
            modules.update({"baseline_harden", "drift_check"})
        return sorted(modules)

