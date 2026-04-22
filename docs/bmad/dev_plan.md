---
artifact: dev_plan
project: HardSecNet PySide
date: 2026-04-22
role: scrum-master
phase: implementation
workflow: bmad-correct-course
---

# Development Plan

## Goal

Complete HardSecNet PySide as a local-first CIS hardening studio. Keep the implementation demonstrable on one machine.

## Milestones

1. Scope Pruning
   - Remove remote control-plane, device-agent, shared-contract, and web-dashboard code.
   - Remove remote orchestration models, tables, dependencies, UI pages, and tests.

2. Local Benchmark Core
   - Preserve benchmark exports.
   - Keep import, script-candidate generation, and seeded bundle loading working.
   - Surface script readiness, risk level, and dry-run evidence for each benchmark control.
   - Seed curated ready-script examples for built-in controls.

3. Local Dashboard Flow
   - Add Dashboard-first current-device posture metrics.
   - Keep the PySide pages focused on current-device operation.
   - Ensure navigation exposes only local pages.
   - Use final local-baseline wording instead of demo wording.

4. Local Run And Drift
   - Preserve profile execution, findings, reports, and comparison deltas.
   - Keep live hardening execution gated behind explicit operator/environment approval.

5. Local AI Explanation
   - Keep AI Advisor and local explanation records.
   - Support optional live Ollama calls inside the local `AgentEngine` boundary.
   - Preserve deterministic fallback for offline demos and tests.

6. Validation
   - Compile source and tests.
   - Run local test suite.
   - Scan source for removed remote/fleet implementation references.

## Acceptance

- `python -m compileall src tests` passes.
- `python -m pytest -q tests` passes.
- No remote services or web dashboard directories remain.
- README and BMAD artifacts define the project as local-only.
- Benchmark scripts are inspectable in the desktop app and dry runs produce traceable local artifacts without applying system changes.
- Built-in controls include ready-script examples, while imported controls can remain review-required until validated.
- Local AI explanations work without network dependencies and can use Ollama when explicitly enabled.
