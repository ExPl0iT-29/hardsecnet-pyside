# HardSecNet PySide First Run

Date: 2026-04-22
Scope: local desktop app only

## Prerequisites

- Windows with PowerShell
- Python 3.12+
- optional Ollama runtime for future live local-AI explanation work

## Setup

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Run The App

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
hardsecnet-pyside
```

The desktop app opens the local HardSecNet operator workspace.

## Suggested First Flow

1. Open `Benchmarks` and confirm the seeded CIS Windows or Ubuntu benchmark bundle is visible.
2. Open `Dashboard` to review current-device posture metrics.
3. Open `Hardening`, choose a profile, and run it.
4. Review findings and run details.
5. Open `AI Advisor` to inspect risk and remediation explanations.
6. Open `Reports` and inspect the generated JSON, HTML, and PDF paths.
7. Run the profile again to generate comparison deltas when prior findings exist.

## Verification

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\python.exe -m compileall src tests
.\.venv\Scripts\python.exe -m pytest -q tests
```

## Runtime Outputs

Generated files appear under:

- `runtime/artifacts/`
- `runtime/reports/`
- `runtime/imports/`
- `runtime/generated_scripts/`

The local SQLite database is `runtime/hardsecnet.db`.
