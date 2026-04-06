---
title: 'v2 fleet control plane foundations'
type: 'feature'
created: '2026-04-04'
status: 'ready-for-dev'
context:
  - 'docs/implementation_proof.md'
  - 'docs/validation.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The current PySide6 app is local-device only. v2 requires real fleet primitives so multiple devices can enroll, report health, receive jobs, upload results, and appear in a dashboard-ready control surface.

**Approach:** Add a fleet control-plane slice inside the current workspace: persistence for fleet state, a service layer for enrollment/heartbeat/job/result flows, and a UI surface that exposes fleet status and campaigns without claiming that the full remote platform is done.

## Boundaries & Constraints

**Always:** Preserve the current local-first app behavior; keep existing run/report flows working; model devices and jobs so later external agents or a web dashboard can reuse the same data; verify with automated tests and runtime smoke checks.

**Ask First:** Replacing the current desktop app with a separate backend repo; introducing destructive remote hardening execution; removing existing local run paths.

**Never:** Claim that full v2 fleet orchestration is complete; fake remote execution; break the existing six app areas without replacing them with a coherent fleet-aware navigation model.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| ENROLL_DEVICE | New device manifest and device metadata | Device is stored, manifest is stored, fleet view includes device | Reject empty ids and unknown OS family with clear error |
| HEARTBEAT | Existing device sends status and queue count | Latest heartbeat is stored and dashboard updates health state | Unknown device returns an explicit error |
| QUEUE_AND_CLAIM_JOB | Approved job exists for a device | Job can be queued, claimed, and marked in progress | No pending job returns `None` without mutating state |
| SUBMIT_JOB_RESULT | Claimed job posts summary and artifacts | Result is recorded and linked to the job/device | Unknown job id raises a clear error |

</frozen-after-approval>

## Code Map

- `src/hardsecnet_pyside/models.py` -- existing v2-oriented dataclasses for devices, jobs, sync envelopes, campaigns
- `src/hardsecnet_pyside/persistence.py` -- SQLite schema and repository methods that need fleet storage extensions
- `src/hardsecnet_pyside/services.py` -- current local orchestration service; needs fleet control-plane integration
- `src/hardsecnet_pyside/app.py` -- controller layer used by the UI and tests
- `src/hardsecnet_pyside/ui/main_window.py` -- navigation shell for adding a fleet-facing view
- `src/hardsecnet_pyside/ui/pages.py` -- current page implementations; add fleet dashboard page here
- `tests/` -- add fleet flow and UI smoke coverage

## Tasks & Acceptance

**Execution:**
- [ ] `src/hardsecnet_pyside/persistence.py` -- add fleet tables and repository methods for heartbeats, jobs, job results, and device-oriented queries -- persistence is the gate for any real v2 state
- [ ] `src/hardsecnet_pyside/services.py` -- add fleet control-plane APIs for enrollment, heartbeat, queue/claim/complete job flows, campaigns, and fleet snapshots -- this is the runtime contract for future agents and dashboards
- [ ] `src/hardsecnet_pyside/app.py` -- expose fleet APIs through the controller without breaking existing local flows -- keeps UI and tests aligned to one surface
- [ ] `src/hardsecnet_pyside/ui/main_window.py` and `src/hardsecnet_pyside/ui/pages.py` -- add a fleet dashboard page showing devices, health, jobs, and campaigns -- creates a visible v2 surface
- [ ] `tests/test_fleet.py` and related test updates -- cover enrollment, heartbeat, queue/claim/result flows, and fleet UI smoke -- verifies the new slice and its edge cases

**Acceptance Criteria:**
- Given a fresh project runtime, when a device is enrolled and heartbeats are recorded, then the fleet dashboard shows the device with current status and queue information.
- Given a queued approved job for a device, when the device claims it and submits a result, then the job transitions through pending to in-progress to completed and the result is queryable.
- Given multiple devices with runs and findings, when the fleet snapshot is requested, then the controller returns aggregated device, job, and campaign state without breaking local reports or local run pages.
- Given the updated project, when automated tests and headless UI smoke are run, then the fleet slice and existing local app flows both pass.

## Verification

**Commands:**
- `E:\T\hardsecnet\hardsecnet-pyside\.venv\Scripts\python.exe -m compileall E:\T\hardsecnet\hardsecnet-pyside\src\hardsecnet_pyside` -- expected: no syntax errors
- `E:\T\hardsecnet\hardsecnet-pyside\.venv\Scripts\python.exe -m pytest -q E:\T\hardsecnet\hardsecnet-pyside\tests` -- expected: all tests pass
- `QT_QPA_PLATFORM=offscreen ... build main window` -- expected: fleet page loads and dashboard status renders
