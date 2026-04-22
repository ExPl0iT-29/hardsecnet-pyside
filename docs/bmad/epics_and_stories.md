---
artifact: epics_and_stories
project: HardSecNet PySide
date: 2026-04-22
role: scrum-master
phase: implementation-planning
workflow: bmad-create-epics-and-stories
bmadVersion: v6-overlay-requested
bmadProjectMode: upstream-bmad-v6-requested
migrationStatus: config-missing
compatibilityMode: false
enabledModules:
  - core
  - bmm
  - bmb
  - cis
stepsCompleted:
  - validate-prerequisites
  - decompose-prd
  - create-epics
  - create-stories
blockers:
  - _bmad/bmm/config.yaml is missing.
handoffTarget: dev
completionState: ready-for-epic-implementation
---

# HardSecNet Epics And Stories

## Epic 1: Benchmark Native Mode

Goal:

- make exported CIS bundles available inside the app automatically, without needing the PDFs or manual import.

### Story 1.1: Discover Exported Benchmark Bundles

As a developer, I want the app to discover benchmark export bundles on startup so that repo-owned benchmark data becomes available automatically.

Acceptance criteria:

- scans `src/hardsecnet_pyside/data/benchmark_exports/`
- detects directories with `benchmark_document.json` and `benchmark_items.json`
- ignores malformed folders with a clear warning
- unit tests cover valid and invalid bundle folders

### Story 1.2: Load Exported Bundles Into Local Repository

As an operator, I want Windows and Ubuntu CIS controls loaded automatically so I do not need to import PDFs.

Acceptance criteria:

- fresh runtime DB includes Windows CIS document
- fresh runtime DB includes Ubuntu CIS document
- duplicate bootstrap does not create duplicate documents
- provenance includes bundle path and script directory

### Story 1.3: Preserve Generated Script Paths

As an operator, I want each control to link to its generated script candidate so review can start from the UI.

Acceptance criteria:

- each loaded control has script path metadata
- missing script path is represented as review issue, not crash
- tests confirm at least one Windows and one Ubuntu control resolves a script path

## Epic 2: Benchmark Browser And Review UI

Goal:

- make benchmark controls inspectable and reviewable from the desktop app.

### Story 2.1: Add Benchmark Browser Page

As an operator, I want to browse benchmark controls so I can understand what HardSecNet imported.

Acceptance criteria:

- desktop navigation includes benchmark browser
- table shows ID, title, OS, level, automated/manual, confidence, status
- supports Windows/Ubuntu filtering
- UI smoke test updated

### Story 2.2: Add Control Detail Panel

As an operator, I want to inspect a selected control so I can review rationale, audit, remediation, and source provenance.

Acceptance criteria:

- selecting a control shows detail panel
- panel includes rationale
- panel includes audit notes
- panel includes remediation steps
- panel includes source page and citations

### Story 2.3: Add Script Candidate Preview

As an operator, I want to preview the generated script candidate for a control so I can decide whether it is safe to validate.

Acceptance criteria:

- detail panel shows script path
- script contents can be previewed read-only
- missing script file shows clear error state
- preview does not execute anything

## Epic 3: Script Registry And Validation Workflow

Goal:

- make script lifecycle explicit and enforce safety gates.

### Story 3.1: Add ScriptRecord Model And Persistence

As a developer, I want script records persisted so generated scripts can move through review states.

Acceptance criteria:

- model includes benchmark ID, OS, path, state, reviewer, notes
- persistence table exists
- repository supports list/get/save
- tests cover serialization

### Story 3.2: Add Review State Transitions

As a reviewer, I want to mark scripts as reviewed, validated, rejected, or deprecated.

Acceptance criteria:

- allowed states are enforced
- invalid transitions fail clearly
- reviewer and timestamp are stored
- tests cover valid and invalid transitions

### Story 3.3: Gate Hardening Execution On Validation

As an operator, I want unvalidated scripts blocked from hardening execution so candidate scripts cannot damage systems.

Acceptance criteria:

- hardening jobs reject candidate scripts
- audit jobs may reference candidate scripts
- rejection reason is visible in job result
- tests cover candidate vs validated behavior

## Epic 4: Dashboard Operator Workflows

Goal:

- turn dashboard from read-only view into usable fleet operations surface.

### Story 4.1: Add Dashboard Login Screen

As a dashboard user, I want to log in explicitly so credentials are not hidden in app code.

Acceptance criteria:

- login form exists
- token is stored in memory
- bootstrap behavior is explicit
- login errors are visible

### Story 4.2: Add Device Detail View

As an operator, I want a device detail view so I can inspect one endpoint before taking action.

Acceptance criteria:

- device list supports selecting a device
- detail shows metadata and latest heartbeat
- detail shows jobs and reports for device
- empty states are clear

### Story 4.3: Add Job Creation UI

As an operator, I want to create audit/compare/hardening jobs from the dashboard.

Acceptance criteria:

- form supports action type
- form supports target device
- hardening jobs default to approval required
- created job appears in job list

### Story 4.4: Add Approval Queue UI

As a security admin, I want to approve or reject jobs so risky actions are controlled.

Acceptance criteria:

- pending approval jobs are listed
- approve action calls backend
- reject/cancel action exists or is explicitly not implemented with disabled state
- audit trail is recorded

### Story 4.5: Add Report Detail Viewer

As an auditor, I want to open reports from the dashboard so I can inspect completed work.

Acceptance criteria:

- report list supports selecting report
- detail shows title, summary, device, job, generated paths
- download links are shown when backend supports them

## Epic 5: Agent Operational Mode

Goal:

- make the agent usable as a long-running endpoint process.

### Story 5.1: Add Agent Loop Mode

As an endpoint operator, I want the agent to run continuously so it can receive jobs over time.

Acceptance criteria:

- CLI supports one-shot and loop modes
- interval is configurable
- loop logs each poll cycle
- Ctrl+C exits cleanly

### Story 5.2: Add Agent Config File

As an operator, I want agent settings in a file so service deployment does not depend only on environment variables.

Acceptance criteria:

- config file path can be passed
- env vars override file values
- docs include example config
- tests cover loading precedence

### Story 5.3: Add Offline Queue

As an endpoint operator, I want results queued locally when backend is unavailable.

Acceptance criteria:

- failed result submissions are written to state dir
- later poll attempts retry queued results
- retry failure does not delete queue item
- tests cover retry behavior

## Epic 6: Reports And Artifacts

Goal:

- make reports and artifacts first-class API/dashboard objects.

### Story 6.1: Add Report Detail API

As a dashboard user, I want full report details through the API.

Acceptance criteria:

- endpoint returns report metadata
- endpoint includes linked job and device IDs
- endpoint returns artifact paths
- RBAC enforced

### Story 6.2: Add Artifact Download API

As an auditor, I want to download generated report artifacts.

Acceptance criteria:

- JSON artifact download works
- HTML artifact download works
- PDF artifact download works
- invalid path traversal is blocked

### Story 6.3: Add Dashboard Report Viewer

As an auditor, I want to open report details and download artifacts from the dashboard.

Acceptance criteria:

- report detail page exists
- download actions call backend
- missing artifact shows clear state

## Epic 7: Validated Hardening Modules

Goal:

- convert high-value generated candidates into real validated hardening modules.

### Story 7.1: Validate First Ubuntu Controls

As a developer, I want to validate the first Ubuntu scripts so HardSecNet has real runnable Linux value.

Acceptance criteria:

- select first 20 high-value Ubuntu controls
- scripts include audit/apply/verify modes
- scripts include rollback notes
- tests or dry-run smoke checks exist

### Story 7.2: Validate First Windows Controls

As a developer, I want to validate the first Windows policy controls so HardSecNet has real runnable Windows value.

Acceptance criteria:

- select first 10 Windows controls
- scripts use PowerShell/secedit/registry where appropriate
- scripts include audit/apply/verify modes
- rollback notes exist

## Epic 8: Packaging And Release Hardening

Goal:

- make the project easier to run and distribute.

### Story 8.1: Add `.env.example`

As a new developer, I want example environment files so I know what to configure.

Acceptance criteria:

- backend env vars documented
- agent env vars documented
- dashboard env vars documented

### Story 8.2: Add Deployment Runbooks

As an operator, I want deployment docs so I can run each surface outside development.

Acceptance criteria:

- backend runbook exists
- dashboard production build runbook exists
- agent service runbook exists

### Story 8.3: Add Release Checklist

As a maintainer, I want a release checklist so quality gates are explicit.

Acceptance criteria:

- tests listed
- build steps listed
- known manual checks listed
- generated-script safety warning included

## First Recommended Sprint

Sprint goal:

- implement Epic 1 completely and start Epic 2.

Stories:

- Story 1.1
- Story 1.2
- Story 1.3
- Story 2.1

Why:

- it makes the CIS work visible and native in the app
- it unlocks script review
- it is the shortest path to making the product feel real

## BMAD Checkpoint

- Role: `scrum-master`
- Phase: `implementation-planning`
- Workflow: `bmad-create-epics-and-stories`
- Artifact created: `docs/bmad/epics_and_stories.md`
- Blockers:
  - `_bmad/bmm/config.yaml` missing
  - open decision on Ubuntu-first vs Windows-first script validation
- Decisions:
  - first sprint starts with benchmark native mode
  - dashboard operator flows come after benchmark visibility
  - validated scripts are separate from generated candidates
- Handoff target: `dev`
- Completion state: `ready-for-epic-implementation`
