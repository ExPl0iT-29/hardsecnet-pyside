# HardSecNet PySide6

`hardsecnet-pyside` is the new desktop workbench for HardSecNet.

It is designed as a benchmark-aware hardening studio for Windows and Linux with:

- built-in and imported benchmark profiles
- approval-gated hardening orchestration
- explainable AI-assisted reasoning
- JSON, HTML, and PDF reporting
- local SQLite history ready for future fleet synchronization
- a FastAPI control plane for fleet orchestration
- a Python device agent for managed endpoints
- a React dashboard for live fleet visibility

## Monorepo Layout

- `src/hardsecnet_pyside/`: PySide6 desktop operator app
- `services/control_plane/`: FastAPI control plane and Alembic migrations
- `services/device_agent/`: Python endpoint agent
- `shared/contracts/`: shared cross-process models
- `web/dashboard/`: React + Vite fleet dashboard

## Desktop App

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
hardsecnet-pyside
```

## Control Plane

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_CP_DATABASE_URL = "sqlite:///./runtime/control_plane.db"
$env:HARDSECNET_CP_ARTIFACTS_DIR = ".\\runtime\\control_plane_artifacts"
.\.venv\Scripts\python.exe -m uvicorn services.control_plane.app.main:app --reload
```

## Device Agent

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_AGENT_CONTROL_PLANE_URL = "http://127.0.0.1:8000"
$env:HARDSECNET_AGENT_DEVICE_ID = "agent-01"
$env:HARDSECNET_AGENT_DEVICE_NAME = "Agent 01"
$env:HARDSECNET_AGENT_OS_FAMILY = "windows"
.\.venv\Scripts\python.exe -m services.device_agent.hardsecnet_device_agent.main
```

## Dashboard

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm install
npm run dev
```

## Verification

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\python.exe -m pytest -q tests
```

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm run build
```

See:

- `docs/implementation_proof_full_platform.md`
- `docs/validation_full_platform.md`
