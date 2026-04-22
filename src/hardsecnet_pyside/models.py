from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, is_dataclass
from datetime import UTC, datetime
from typing import Any


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _json_default(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if is_dataclass(value):
        return asdict(value)
    raise TypeError(f"Unsupported JSON value: {type(value)!r}")


def to_json(data: Any) -> str:
    return json.dumps(data, default=_json_default, indent=2, sort_keys=True)


@dataclass(slots=True)
class EvidenceField:
    name: str
    description: str
    required: bool = True


@dataclass(slots=True)
class DeviceRecord:
    id: str
    name: str
    os_family: str
    hostname: str
    last_seen: str = field(default_factory=utc_now)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BenchmarkDocument:
    id: str
    name: str
    version: str
    os_family: str
    source_type: str
    source_path: str
    source_hash: str
    imported_at: str = field(default_factory=utc_now)
    status: str = "review_required"
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BenchmarkSection:
    id: str
    document_id: str
    title: str
    order_index: int
    page_start: int | None = None
    page_end: int | None = None


@dataclass(slots=True)
class CheckLogic:
    kind: str
    target: str
    operator: str = "equals"
    expected: Any = None
    notes: str = ""


@dataclass(slots=True)
class RemediationStep:
    title: str
    command: str
    expected_impact: str
    rollback: str
    approval_required: bool = True


@dataclass(slots=True)
class BenchmarkItem:
    id: str
    document_id: str
    benchmark_id: str
    title: str
    os_family: str
    profile_level: str = "L1"
    automated: bool = False
    rationale: str = ""
    recommendation: str = ""
    audit_logic: list[CheckLogic] = field(default_factory=list)
    remediation_steps: list[RemediationStep] = field(default_factory=list)
    rollback_notes: list[str] = field(default_factory=list)
    evidence_fields: list[EvidenceField] = field(default_factory=list)
    source_page: int | None = None
    citations: list[str] = field(default_factory=list)
    confidence: float = 0.5
    status: str = "review_required"
    tags: list[str] = field(default_factory=list)
    candidate_modules: list[str] = field(default_factory=list)
    script_path: str = ""
    script_state: str = "unmapped"
    review_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScriptReadiness:
    item_id: str
    document_id: str
    benchmark_id: str
    title: str
    os_family: str
    script_path: str = ""
    status: str = "missing"
    reason: str = ""
    risk_level: str = "medium"
    commands_preview: list[str] = field(default_factory=list)
    rollback_notes: list[str] = field(default_factory=list)
    review_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ScriptExecutionRecord:
    id: str
    benchmark_item_id: str
    benchmark_id: str
    document_id: str
    mode: str
    status: str
    command: str = ""
    output: str = ""
    error: str = ""
    artifact_path: str = ""
    operator: str = "operator"
    allow_execute: bool = False
    readiness_status: str = ""
    risk_level: str = ""
    created_at: str = field(default_factory=utc_now)
    completed_at: str = ""


@dataclass(slots=True)
class ControlMapping:
    id: str
    benchmark_item_id: str
    os_family: str
    module_ids: list[str]
    check_logic: list[CheckLogic] = field(default_factory=list)
    remediation_steps: list[RemediationStep] = field(default_factory=list)
    evidence_fields: list[EvidenceField] = field(default_factory=list)
    confidence: float = 0.5
    approval_state: str = "review_required"


@dataclass(slots=True)
class ProfileTemplate:
    id: str
    name: str
    os_family: str
    description: str
    benchmark_ids: list[str]
    module_ids: list[str]
    strictness: str
    built_in: bool = False
    review_required: bool = False


@dataclass(slots=True)
class ModuleDefinition:
    id: str
    name: str
    description: str
    os_families: list[str]
    default_enabled: bool = True


@dataclass(slots=True)
class StepResult:
    stage: str
    status: str
    message: str
    command: str = ""
    artifact_paths: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    started_at: str = field(default_factory=utc_now)
    ended_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class ModuleResult:
    module_id: str
    title: str
    steps: list[StepResult] = field(default_factory=list)
    benchmark_refs: list[str] = field(default_factory=list)
    manual: bool = False


@dataclass(slots=True)
class RunRecord:
    id: str
    device_id: str
    profile_id: str
    os_family: str
    status: str
    started_at: str = field(default_factory=utc_now)
    ended_at: str = ""
    modules: list[str] = field(default_factory=list)
    module_results: list[ModuleResult] = field(default_factory=list)
    raw_artifacts: list[str] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ComplianceFinding:
    id: str
    run_id: str
    benchmark_id: str
    title: str
    status: str
    severity: str
    evidence: list[str]
    expected: str = ""
    actual: str = ""
    source_page: int | None = None
    module_id: str = ""
    remediation: list[str] = field(default_factory=list)
    rollback: list[str] = field(default_factory=list)
    rationale: str = ""
    citations: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass(slots=True)
class ComparisonDelta:
    id: str
    device_id: str
    before_run_id: str
    after_run_id: str
    benchmark_id: str
    title: str
    delta_type: str
    before_status: str
    after_status: str
    summary: str


@dataclass(slots=True)
class ReportBundle:
    id: str
    run_id: str
    comparison_id: str
    title: str
    generated_at: str = field(default_factory=utc_now)
    json_path: str = ""
    html_path: str = ""
    pdf_path: str = ""
    executive_summary: str = ""
    technical_summary: str = ""


@dataclass(slots=True)
class ApprovalRecord:
    id: str
    target_type: str
    target_id: str
    decision: str
    reviewer: str
    notes: str = ""
    decided_at: str = field(default_factory=utc_now)


@dataclass(slots=True)
class AgentRecommendation:
    benchmark_reference: str
    evidence_used: list[str]
    confidence: float
    proposed_action: str
    expected_impact: str
    rollback_path: str
    approval_state: str
    explanation: str


@dataclass(slots=True)
class AITaskRecord:
    id: str
    agent_type: str
    subject_type: str
    subject_id: str
    provider: str
    status: str
    prompt_hash: str
    result: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    completed_at: str = ""


@dataclass(slots=True)
class NetworkCheck:
    id: str
    title: str
    status: str
    details: str
    benchmark_refs: list[str] = field(default_factory=list)
