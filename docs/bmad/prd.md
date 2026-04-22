---
artifact: prd
project: HardSecNet PySide
date: 2026-04-22
role: pm
phase: planning
workflow: bmad-correct-course
---

# Product Requirements Document

## Product Definition

HardSecNet PySide is a local-first CIS hardening studio for Windows and Linux. It runs on the current operator device and helps the user import benchmark controls, review mapped scripts, run local audit/hardening profiles, compare before/after drift, explain risk through local AI, and export evidence-backed reports.

## Scope

### In Scope

- CIS benchmark document import and seeded benchmark bundles.
- Benchmark item browsing with traceability to generated script candidates.
- Local current-device dashboard workflow.
- First-page local posture dashboard with benchmark, run, review, drift, AI, and report metrics.
- Local profile execution and deterministic audit/hardening scaffolding.
- Before/after drift comparison between runs.
- Local AI risk, remediation, and approval explanation records with Ollama-oriented configuration.
- JSON, HTML, and PDF report export.
- Windows and Linux support within one desktop app.

### Out Of Scope

- Parent admin PC controlling child PCs.
- Remote enrollment, heartbeat, or child-device agent loops.
- Remote job queues.
- Remote campaigns.
- Web fleet dashboard.
- Multi-device orchestration.
- Cloud AI dependency.

## Users

- A student/operator demonstrating benchmark-aligned hardening on a local machine.
- A security learner who needs to understand why a CIS control matters and what a remediation may affect.
- A reviewer who needs reportable evidence, drift deltas, and approval notes.

## Core Requirements

1. The app must work without a server.
2. The app must show benchmark documents and controls.
3. The app must run a selected local profile and persist the run.
4. The app must create findings tied to benchmark IDs and evidence.
5. The app must compare current and previous local runs when prior data exists.
6. The app must expose AI explanation records for risk and remediation review.
7. The app must export reports locally.
8. The app must not require multiple PCs to demonstrate the project.

## Success Criteria

- Desktop app launches and renders seven local pages with Dashboard first.
- Seeded CIS Windows and Ubuntu benchmark exports load.
- A profile run creates run, finding, approval, AI task, and report records.
- Tests pass for the local benchmark/controller/UI surface.
- No control-plane, remote-agent, web-dashboard, or fleet-control code remains in the repo.
