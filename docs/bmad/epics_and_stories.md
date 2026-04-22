---
artifact: epics_and_stories
project: HardSecNet PySide
date: 2026-04-22
role: scrum-master
phase: implementation
workflow: bmad-correct-course
---

# Epics And Stories

## Epic 1: Benchmark Library

Story 1.1: Load seeded CIS benchmark exports.

Story 1.2: Import new benchmark source files and generate structured controls.

Story 1.3: Generate reviewable script candidates with benchmark traceability.

## Epic 2: Local Profile Execution

Story 2.1: Select a current-device profile from the desktop app.

Story 2.2: Run local deterministic audit/hardening scaffolding.

Story 2.3: Persist runs, findings, module results, and approvals.

## Epic 3: Drift Comparison

Story 3.1: Compare current findings against the previous local run.

Story 3.2: Show improved, regressed, changed, and unchanged posture movement.

Story 3.3: Include drift details in exported reports.

## Epic 4: Local AI Explanation

Story 4.1: Explain risk and expected effect for benchmark findings.

Story 4.2: Produce remediation and approval recommendations.

Story 4.3: Prepare `AgentEngine` for live Ollama calls without introducing cloud or server dependencies.

## Epic 5: Reporting

Story 5.1: Export JSON report bundles.

Story 5.2: Export readable HTML reports.

Story 5.3: Export PDF reports when PyMuPDF is available.

## Epic 6: Desktop UX

Story 6.1: Provide local pages for Dashboard, Hardening, Network, AI Advisor, Reports, Benchmarks, and Settings.

Story 6.2: Remove all remote/fleet controls from navigation and UI.

Story 6.3: Keep status and settings focused on local runtime state.

## Epic 7: Validation

Story 7.1: Compile local source and tests.

Story 7.2: Run local tests.

Story 7.3: Verify removed remote surfaces are absent from implementation directories.
