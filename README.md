# HardSecNet PySide

HardSecNet PySide is a local-first CIS hardening studio for Windows and Linux. It keeps the project focused on one operator machine: import or use CIS benchmark controls, map them to reviewable scripts, run local audit/hardening flows, compare drift, explain risk with local AI, and export evidence-backed reports.

Fleet control is not part of this project scope. There is no parent admin PC, child PC agent, control plane, remote job queue, or web fleet dashboard in this repo.

## What This Repo Is For

HardSecNet PySide solves the local hardening workflow:

- import CIS benchmark sources and normalize controls
- maintain benchmark-to-script traceability
- run local benchmark-aware profiles for Windows and Linux
- capture before/after drift and explain its effect
- produce local JSON, HTML, and PDF reports
- keep AI explanation local-first through the Ollama-oriented settings path

The exported scripts are reviewable candidates, not blind production remediations. Operators should approve and validate commands before applying them to live machines.

## Current Status

What works today:

- polished local Dashboard page for current-device posture
- PySide6 desktop app shell
- local benchmark import and durable benchmark exports
- script readiness review with risk, command preview, and dry-run artifacts
- curated ready script examples for local baseline validation
- local run/report flow with findings and comparison deltas
- local AI task records with deterministic fallback and optional Ollama-backed risk/report explanations
- Windows and Ubuntu CIS benchmark bundles stored in the repo

What is still incomplete:

- many Windows generated scripts remain policy templates that need validation
- Ubuntu shell candidates still need systematic production validation
- Ollama-backed live model calls require a running local Ollama server and `HARDSECNET_OLLAMA_LIVE=1`
- packaging and installer hardening are not complete

## Layout

- `src/hardsecnet_pyside/`
  - PySide app, controller/service logic, benchmark import, reports, AI explanation scaffolding
- `src/hardsecnet_pyside/data/benchmark_exports/`
  - extracted CIS benchmark bundles and generated script candidates
- `runtime/`
  - local generated artifacts, imports, reports, scripts, and SQLite state
- `docs/`
  - BMAD artifacts, architecture, validation notes, onboarding, and benchmark docs
- `original_docs/`
  - source planning/reference documents retained for project provenance

## New User Quick Start

Read these in order:

1. [First Run Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/FIRST_RUN.md)
2. [Architecture Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/ARCHITECTURE_GUIDE.md)
3. [CIS Benchmark Engine](/E:/T/hardsecnet/hardsecnet-pyside/docs/CIS_BENCHMARK_ENGINE.md)
4. [Validation Summary](/E:/T/hardsecnet/hardsecnet-pyside/docs/validation.md)

## Environment

Expected developer environment:

- Windows with PowerShell
- Python 3.12+
- PyMuPDF through project dependencies for PDF parsing
- optional local Ollama runtime for future live local-AI explanation work

## Setup

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run The Desktop App

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
hardsecnet-pyside
```

The app provides:

- current-device dashboard metrics
- local CIS benchmark browsing/import
- generated script readiness and guarded dry runs
- curated ready-script examples for built-in benchmark controls
- local profile execution
- current-device dashboard flow
- before/after drift comparison
- AI Advisor records for risk and remediation explanation
- local report export

Optional live local AI:

```powershell
$env:HARDSECNET_OLLAMA_LIVE = "1"
$env:HARDSECNET_LOCAL_MODEL = "phi3"
hardsecnet-pyside
```

When Ollama is unavailable or disabled, the app falls back to deterministic local explanations.

## Verification

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\python.exe -m pytest -q tests
```

## Benchmark Exports

The extracted CIS benchmark bundles live in the repo:

- [Windows 11 CIS Export](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-microsoft-windows-11-stand-alone-benchmark-v4.0.0)
- [Ubuntu 24.04 CIS Export](/E:/T/hardsecnet/hardsecnet-pyside/src/hardsecnet_pyside/data/benchmark_exports/cis-ubuntu-linux-24.04-lts-benchmark-v1.0.0)

Each bundle contains:

- `benchmark_document.json`
- `benchmark_items.json`
- `scripts/`
- `README.md`

The desktop app no longer needs the original PDFs at runtime for these two imported benchmark sets.

## Caveat

Treat generated scripts as:

- benchmark-derived candidates
- traceable starting points
- review-required implementation inputs

Do not run every generated script on a live machine without review.

## Supporting Docs

- [First Run Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/FIRST_RUN.md)
- [Architecture Guide](/E:/T/hardsecnet/hardsecnet-pyside/docs/ARCHITECTURE_GUIDE.md)
- [CIS Benchmark Engine](/E:/T/hardsecnet/hardsecnet-pyside/docs/CIS_BENCHMARK_ENGINE.md)
- [Implementation Proof](/E:/T/hardsecnet/hardsecnet-pyside/docs/implementation_proof.md)
- [Validation](/E:/T/hardsecnet/hardsecnet-pyside/docs/validation.md)
