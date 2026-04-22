---
artifact: scope_realignment
project: HardSecNet PySide
date: 2026-04-22
role: analyst
phase: scope-pruning
workflow: bmad-correct-course
---

# Scope Realignment

## Authoritative Scope

HardSecNet PySide is a software-only, local-first CIS hardening studio. It must be demonstrable on one device.

## Keep

- CIS benchmark bundles and imports.
- Generated/reviewable scripts.
- Current-device dashboard flow.
- Local profile execution.
- Local drift comparison.
- Local AI explanation with Ollama-oriented settings.
- Local JSON, HTML, and PDF reporting.

## Remove

- Remote control plane.
- Child-device agent.
- Shared remote API contracts.
- Web dashboard.
- Remote job queues.
- Campaign management.
- Multi-device orchestration.

## Result

The repository was pruned so the remaining implementation matches the project that can be completed and defended without a multi-PC lab.
