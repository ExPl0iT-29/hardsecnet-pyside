---
artifact: prd
project: HardSecNet PySide
date: 2026-04-22
role: pm
phase: planning
workflow: bmad-create-prd
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
  - restore-project-state
  - confirm-current-product-state
  - define-remaining-product-scope
  - create-prd
blockers:
  - _bmad/bmm/config.yaml is missing, so this artifact follows the BMAD structure manually.
handoffTarget: architect
completionState: drafted
---

# HardSecNet Remaining Product Requirements

## 1. Product Summary

HardSecNet is a local-first hardening and fleet security platform for Windows and Linux.

The current repo already contains:

- PySide6 desktop app
- FastAPI control plane
- Python device agent
- React dashboard
- CIS PDF extraction and exported benchmark bundles
- generated Windows and Ubuntu script candidates

The next product phase is about turning this working platform slice into something a new operator can use end to end without developer hand-holding.

The core remaining product promise:

> A user can browse CIS controls, review generated remediation scripts, approve safe actions, execute audits/hardening through agents, and produce traceable reports across local and fleet contexts.

## 2. Target Users

### Security Operator

Needs to:

- see device posture
- run audit jobs
- approve remediation
- review evidence
- export reports

### System Administrator

Needs to:

- understand what a hardening action will change
- review rollback notes
- run scripts safely
- avoid breaking endpoints

### Developer / Contributor

Needs to:

- understand repo surfaces quickly
- validate generated scripts
- add checks and adapters
- extend dashboard and desktop workflows

### Auditor / Reviewer

Needs to:

- trace a finding to a CIS control
- see evidence and source citation
- understand before/after deltas
- export reports

## 3. Current Product Gaps

### 3.1 CIS Benchmark Data Is Not Native Enough

The extracted CIS bundles exist in the repo, but the app does not yet treat them as first-class built-in benchmark sources.

Required:

- auto-load exported bundles on startup
- show benchmark documents and controls in UI
- preserve source page, rationale, audit, remediation, confidence, and script path
- expose review state per control

### 3.2 Generated Scripts Are Not Validated Modules

The current generated scripts are candidates.

Required:

- mark scripts as candidate/reviewed/validated/deprecated
- convert priority Ubuntu scripts into runnable modules
- convert priority Windows policy templates into real PowerShell/secedit/registry logic
- add rollback metadata
- add dry-run mode

### 3.3 Dashboard Is Too Read-Only

The dashboard currently shows data, but it does not support enough operator action.

Required:

- login screen
- device detail
- job creation
- approval queue
- report viewer
- benchmark/profile views
- campaign creation

### 3.4 Agent Is One-Shot

The agent can poll once, but a fleet agent needs a long-running mode.

Required:

- loop mode
- config file
- offline queue
- retry policy
- privilege checks
- service packaging

### 3.5 Control Plane Needs Product-Grade APIs

The API has the skeleton, but needs production behavior.

Required:

- report download endpoints
- artifact access
- audit log API
- pagination/filtering
- RBAC negative test coverage
- PostgreSQL deployment path

## 4. Goals

### Goal 1: Make Benchmarks First-Class

Users can browse CIS benchmark controls and understand how each maps to scripts, checks, evidence, and profiles.

Success criteria:

- Windows and Ubuntu bundles auto-load without PDFs
- controls are searchable
- every control shows source and generated script
- review status is visible

### Goal 2: Make Execution Safe

Users can distinguish candidate scripts from validated hardening actions.

Success criteria:

- no candidate script is executed silently
- validated modules include audit, apply, verify, rollback, and dry-run behavior
- approval is required for hardening

### Goal 3: Make Dashboard Useful

Dashboard supports fleet actions, not just visibility.

Success criteria:

- user can create jobs
- user can approve jobs
- user can inspect reports
- user can view device details

### Goal 4: Make Agent Operational

Agent can run continuously and survive temporary backend/network failure.

Success criteria:

- loop mode works
- offline queue retries
- local state survives restart
- agent can be packaged as a service later

### Goal 5: Make Reports Traceable

Reports connect device state to benchmark controls, evidence, and remediation.

Success criteria:

- report links findings to benchmark ID and source page
- report includes script/action used
- report includes approval and rollback metadata

## 5. Non-Goals For This Phase

- fully autonomous AI hardening
- cloud SaaS multi-tenant deployment
- support for every CIS benchmark family
- running generated scripts without validation
- replacing the legacy Windows/Linux script stacks completely

## 6. Functional Requirements

### FR1: Built-In Benchmark Bundle Loader

The app must load exported benchmark bundles from:

- `src/hardsecnet_pyside/data/benchmark_exports/`

The loader must:

- read `benchmark_document.json`
- read `benchmark_items.json`
- index controls by OS family and benchmark ID
- avoid duplicate imports
- preserve provenance and generated script paths

### FR2: Benchmark Browser UI

The desktop app must provide a benchmark/control browser.

Minimum fields:

- benchmark ID
- title
- OS
- profile level
- automated/manual
- confidence
- source page
- status
- candidate modules
- generated script path

### FR3: Control Detail View

The UI must show:

- rationale
- audit guidance
- remediation guidance
- rollback notes
- evidence fields
- script candidate

### FR4: Script Validation Workflow

A script must have explicit lifecycle state:

- candidate
- reviewed
- validated
- rejected
- deprecated

Only `validated` scripts can be used for hardening execution without extra override.

### FR5: Dashboard Login

Dashboard must not hardcode `admin/admin` as invisible behavior.

It must show:

- login form
- bootstrap path for dev/admin first run
- error messages

### FR6: Dashboard Device Detail

Users must inspect:

- device metadata
- heartbeat status
- jobs
- reports
- latest findings

### FR7: Dashboard Job Creation

Users must create:

- audit jobs
- hardening jobs
- compare jobs

Hardening jobs require approval.

### FR8: Approval Queue

Users must see:

- pending jobs
- risky actions
- script validation state
- approve/reject buttons
- audit trail entry after decision

### FR9: Agent Loop Mode

Agent must support:

- one-shot mode
- loop mode
- configurable interval
- graceful shutdown
- retry behavior

### FR10: Report Detail And Download

Users must view and download:

- JSON report
- HTML report
- PDF report
- artifacts

## 7. Non-Functional Requirements

### Safety

- hardening requires explicit approval
- candidate scripts cannot run by default
- rollback notes are mandatory for validated hardening modules

### Traceability

- every finding links to benchmark ID
- every benchmark item links to source page when available
- every report includes device, profile, run, findings, evidence, and approvals

### Reliability

- agent should tolerate backend downtime
- dashboard should show actionable errors
- backend should not lose job results on transient failures

### Developer Experience

- new developer can run tests and dashboard from README
- docs must explain what is scaffold, what is validated, and what is candidate

## 8. Release Milestones

### Milestone 1: Benchmark Native Mode

- auto-load benchmark bundles
- benchmark browser
- control detail view
- tests

### Milestone 2: Script Validation And Execution

- script lifecycle model
- first validated Ubuntu scripts
- first validated Windows scripts
- dry-run and rollback fields

### Milestone 3: Dashboard Operator Workflows

- login
- device detail
- job creation
- approvals
- report detail

### Milestone 4: Agent Operational Mode

- loop mode
- config file
- offline queue
- retries

### Milestone 5: Production Hardening

- report downloads
- artifact endpoints
- audit log viewer
- PostgreSQL docs/tests
- packaging docs

## 9. Open Decisions

- Which OS gets validated script priority first: Ubuntu or Windows?
- Should dashboard become the primary operator UI, or should PySide remain primary?
- Should generated script validation state live in SQLite only, or as repo-side metadata too?
- Should AI be used for script validation suggestions in this phase, or deferred?

## 10. BMAD Checkpoint

- Role: `pm`
- Phase: `planning`
- Workflow: `bmad-create-prd`
- Artifact created: `docs/bmad/prd.md`
- Blockers:
  - `_bmad/bmm/config.yaml` missing
  - no interactive BMAD step menus executed because user requested artifact creation directly
- Decisions:
  - define remaining work as product backlog, not vague “polish”
  - treat generated scripts as candidates until validated
  - prioritize benchmark-native workflow before deeper execution
- Handoff target: `architect`
- Completion state: `drafted`
