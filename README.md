# HardSecNet PySide

HardSecNet is a local-first cross-platform hardening studio and fleet prototype for Windows and Linux.

This repo currently contains four product surfaces:

- a `PySide6` desktop operator app
- a `FastAPI` control plane
- a Python device agent
- a `React + Vite` fleet dashboard

It also contains a CIS benchmark ingestion pipeline that can extract controls from benchmark source files, normalize them into structured records, and generate reviewable script candidates.

## What This Repo Is For

HardSecNet is trying to solve a specific problem:

- import hardening benchmarks like CIS
- convert them into structured controls
- map those controls to local checks and remediation steps
- run audits and hardening workflows on Windows and Linux
- store evidence and reports
- eventually coordinate those workflows across multiple devices

This matters because most security hardening tools are either:

- benchmark viewers with weak execution
- execution tools with weak traceability
- enterprise products that are difficult to adapt locally

HardSecNet is trying to keep benchmark traceability, execution flexibility, and local control in one place.

## Current Status

What works today:

- desktop app shell and local reporting flow
- control plane API with auth, devices, jobs, campaigns, and reports
- device agent polling flow
- web dashboard build and API integration
- CIS benchmark extraction from the provided Windows and Ubuntu PDFs
- durable benchmark export into the repo as JSON + script candidate bundles

What is still incomplete:

- many generated Windows scripts are still review templates, not fully validated runnable remediations
- Ubuntu script candidates are stronger, but still need systematic validation before production use
- dashboard UX is basic
- production deployment and packaging are not fully hardened yet

## Monorepo Layout

- `src/hardsecnet_pyside/`
  - desktop app, local benchmark/reporting flow, controller/service logic
- `services/control_plane/`
  - FastAPI backend, persistence models, auth, fleet APIs
- `services/device_agent/`
  - polling endpoint agent that talks to the control plane
- `shared/contracts/`
  - shared API/data contracts used across processes
- `web/dashboard/`
  - React fleet dashboard
- `src/hardsecnet_pyside/data/benchmark_exports/`
  - extracted benchmark bundles that no longer depend on the original PDFs at runtime
- `docs/`
  - implementation notes, validation, architecture, onboarding, and benchmark docs

## New User Quick Start

If you are new to the project, read these in order:

1. [First Run Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/FIRST_RUN.md)
2. [Architecture Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/ARCHITECTURE_GUIDE.md)
3. [CIS Benchmark Engine](/E:/T/hardsecnet/hardsecnet-pyside/docs/CIS_BENCHMARK_ENGINE.md)
4. [Validation Summary](/E:/T/hardsecnet/hardsecnet-pyside/docs/validation_full_platform.md)

## Environment

Expected developer environment:

- Windows with PowerShell
- Python 3.12+
- Node.js 18+
- npm

Optional but useful:

- PyMuPDF installed through project dependencies for PDF parsing
- a local AI runtime if you want to extend the AI features

## Setup

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

Dashboard dependencies:

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm install
```

## Run The Surfaces

### 1. Desktop App

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
hardsecnet-pyside
```

What it does:

- local benchmark import
- local run/report flow
- benchmark-aware operator UI
- backend-aware fleet integration when the control plane is configured

### 2. Control Plane

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_CP_DATABASE_URL = "sqlite:///./runtime/control_plane.db"
$env:HARDSECNET_CP_ARTIFACTS_DIR = ".\\runtime\\control_plane_artifacts"
.\.venv\Scripts\python.exe -m uvicorn services.control_plane.app.main:app --reload
```

Default local API:

- `http://127.0.0.1:8000`
- OpenAPI docs at `http://127.0.0.1:8000/docs`

### 3. Device Agent

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_AGENT_URL = "http://127.0.0.1:8000"
$env:HARDSECNET_AGENT_DEVICE_ID = "agent-01"
$env:HARDSECNET_AGENT_DEVICE_NAME = "Agent 01"
$env:HARDSECNET_AGENT_OS = "windows"
.\.venv\Scripts\python.exe -m services.device_agent.hardsecnet_device_agent.main
```

The agent will:

- bootstrap/login to the control plane
- enroll if needed
- send heartbeats
- poll approved jobs
- run adapter-backed work
- upload results

### 4. Dashboard

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm run dev
```

By default the dashboard expects:

- API base: `http://127.0.0.1:8000/api/v1`

You can override it with:

```powershell
$env:VITE_HARDSECNET_API = "http://127.0.0.1:8000/api/v1"
```

## Verification

Python tests:

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\python.exe -m pytest -q tests
```

Dashboard production build:

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm run build
```

## Benchmark Exports

The extracted CIS benchmark bundles now live in the repo:

- [Windows 11 CIS Export](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-microsoft-windows-11-stand-alone-benchmark-v4.0.0)
- [Ubuntu 24.04 CIS Export](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-ubuntu-linux-24.04-lts-benchmark-v1.0.0)

Each bundle contains:

- `benchmark_document.json`
- `benchmark_items.json`
- `scripts/`
- `README.md`

These are durable project artifacts. The application no longer needs the original PDFs at runtime for these two imported benchmark sets.

## Important Caveat

The exported scripts are not all production-safe remediations yet.

That distinction matters.

Many Ubuntu controls extracted into shell-oriented steps fairly well.
Many Windows controls extracted into reviewable policy templates rather than directly runnable PowerShell.

Treat the generated scripts as:

- benchmark-derived candidates
- traceable starting points
- review-required implementation inputs

Not as “blindly run all of them on a live machine”.

## Supporting Docs

- [First Run Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/FIRST_RUN.md)
- [Architecture Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/ARCHITECTURE_GUIDE.md)
- [CIS Benchmark Engine](/E:/T/hardsecnet/hardsecnet-pyside/docs/CIS_BENCHMARK_ENGINE.md)
- [Implementation Proof](/E:/T/hardsecnet/hardsecnet-pyside/docs/implementation_proof_full_platform.md)
- [Validation](/E:/T/hardsecnet/hardsecnet-pyside/docs/validation_full_platform.md)
