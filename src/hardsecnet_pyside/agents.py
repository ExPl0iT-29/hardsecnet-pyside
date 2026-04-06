from __future__ import annotations

import hashlib
from dataclasses import asdict
from typing import Any

from hardsecnet_pyside.config import AISettings
from hardsecnet_pyside.models import (
    AITaskRecord,
    AgentRecommendation,
    BenchmarkDocument,
    BenchmarkItem,
    ComparisonDelta,
    ComplianceFinding,
    ProfileTemplate,
    ReportBundle,
    RunRecord,
    utc_now,
)


class AgentEngine:
    def __init__(self, ai_settings: AISettings) -> None:
        self.ai_settings = ai_settings

    def _task(self, *, agent_type: str, subject_type: str, subject_id: str, result: dict[str, Any]) -> AITaskRecord:
        prompt_hash = hashlib.sha256(
            f"{agent_type}:{subject_type}:{subject_id}:{utc_now()}".encode("utf-8")
        ).hexdigest()
        return AITaskRecord(
            id=f"aitask-{prompt_hash[:12]}",
            agent_type=agent_type,
            subject_type=subject_type,
            subject_id=subject_id,
            provider=self.ai_settings.mode,
            status="completed",
            prompt_hash=prompt_hash,
            result=result,
            completed_at=utc_now(),
        )

    def benchmark_ingestion_agent(
        self, document: BenchmarkDocument, items: list[BenchmarkItem]
    ) -> tuple[AITaskRecord, list[AgentRecommendation]]:
        recommendations = [
            AgentRecommendation(
                benchmark_reference=item.benchmark_id,
                evidence_used=[f"Imported from {document.source_type}", *item.citations],
                confidence=item.confidence,
                proposed_action=f"Review and approve imported control '{item.title}' for {item.os_family}",
                expected_impact="Imported benchmark guidance becomes traceable and reusable inside profiles and reports.",
                rollback_path="Reject or edit the imported control before profile publication.",
                approval_state="review_required",
                explanation="Imported controls remain candidate benchmark items until a human approves the mapping.",
            )
            for item in items[:10]
        ]
        task = self._task(
            agent_type="Benchmark Ingestion Agent",
            subject_type="benchmark_document",
            subject_id=document.id,
            result={"recommendations": [asdict(item) for item in recommendations]},
        )
        return task, recommendations

    def profile_builder_agent(
        self, document: BenchmarkDocument, items: list[BenchmarkItem]
    ) -> tuple[AITaskRecord, list[ProfileTemplate]]:
        profile = ProfileTemplate(
            id=f"profile-{document.id}",
            name=f"{document.name} Imported Baseline",
            os_family=document.os_family,
            description=f"Imported candidate profile built from {document.name}.",
            benchmark_ids=[item.benchmark_id for item in items],
            module_ids=sorted({module for item in items for module in item.candidate_modules}),
            strictness="imported_candidate",
            built_in=False,
            review_required=True,
        )
        task = self._task(
            agent_type="Profile Builder Agent",
            subject_type="benchmark_document",
            subject_id=document.id,
            result={"profiles": [asdict(profile)]},
        )
        return task, [profile]

    def audit_reasoning_agent(
        self, run: RunRecord, findings: list[ComplianceFinding], deltas: list[ComparisonDelta]
    ) -> tuple[AITaskRecord, list[AgentRecommendation]]:
        recommendations: list[AgentRecommendation] = []
        for finding in findings[:12]:
            recommendations.append(
                AgentRecommendation(
                    benchmark_reference=finding.benchmark_id,
                    evidence_used=finding.evidence,
                    confidence=finding.confidence,
                    proposed_action="Investigate and remediate" if finding.status != "Compliant" else "Monitor",
                    expected_impact=f"Move finding state from {finding.status} toward compliant posture.",
                    rollback_path="Review the mapped rollback notes before execution.",
                    approval_state="review_required" if finding.status != "Compliant" else "not_required",
                    explanation=f"Finding '{finding.title}' evaluated as {finding.status}. "
                    f"{'A benchmark delta was detected.' if any(delta.benchmark_id == finding.benchmark_id for delta in deltas) else 'No benchmark delta detected.'}",
                )
            )
        task = self._task(
            agent_type="Audit Reasoning Agent",
            subject_type="run",
            subject_id=run.id,
            result={"recommendations": [asdict(item) for item in recommendations]},
        )
        return task, recommendations

    def remediation_planner_agent(
        self, run: RunRecord, findings: list[ComplianceFinding]
    ) -> tuple[AITaskRecord, list[AgentRecommendation]]:
        recommendations: list[AgentRecommendation] = []
        for finding in findings:
            if finding.status == "Compliant":
                continue
            recommendations.append(
                AgentRecommendation(
                    benchmark_reference=finding.benchmark_id,
                    evidence_used=finding.evidence,
                    confidence=finding.confidence,
                    proposed_action="Queue approval-gated remediation",
                    expected_impact=f"Improve compliance for '{finding.title}'.",
                    rollback_path="Use rollback steps stored in the report bundle and control mapping.",
                    approval_state="approval_required",
                    explanation=f"Remediate '{finding.title}' after human approval. Expected state: {finding.expected or 'compliant'}.",
                )
            )
        task = self._task(
            agent_type="Remediation Planner Agent",
            subject_type="run",
            subject_id=run.id,
            result={"recommendations": [asdict(item) for item in recommendations]},
        )
        return task, recommendations

    def report_writer_agent(
        self, run: RunRecord, findings: list[ComplianceFinding], report: ReportBundle
    ) -> tuple[AITaskRecord, str]:
        compliant = sum(1 for finding in findings if finding.status == "Compliant")
        non_compliant = sum(1 for finding in findings if finding.status != "Compliant")
        summary = (
            f"Run {run.id} completed with {compliant} compliant and {non_compliant} non-compliant findings. "
            f"Report '{report.title}' ties benchmark references, evidence, commands, and rollback notes together."
        )
        task = self._task(
            agent_type="Report Writer Agent",
            subject_type="report",
            subject_id=report.id,
            result={"summary": summary},
        )
        return task, summary

    def approval_gate_agent(
        self, findings: list[ComplianceFinding]
    ) -> tuple[AITaskRecord, list[AgentRecommendation]]:
        recommendations: list[AgentRecommendation] = []
        for finding in findings[:10]:
            risky = any(
                keyword in " ".join(finding.remediation).lower()
                for keyword in ("disable", "remove", "overwrite", "registry")
            )
            recommendations.append(
                AgentRecommendation(
                    benchmark_reference=finding.benchmark_id,
                    evidence_used=finding.evidence,
                    confidence=max(0.6, finding.confidence),
                    proposed_action="Require manual approval" if risky else "Standard review",
                    expected_impact="Reduce unsafe autonomous changes before execution.",
                    rollback_path="Block execution until reviewer approves the mapped action.",
                    approval_state="approval_required" if risky else "review_required",
                    explanation="Risk gate triggered." if risky else "Standard benchmark review is still required.",
                )
            )
        task = self._task(
            agent_type="Approval Gate Agent",
            subject_type="finding_batch",
            subject_id=findings[0].run_id if findings else "none",
            result={"recommendations": [asdict(item) for item in recommendations]},
        )
        return task, recommendations
