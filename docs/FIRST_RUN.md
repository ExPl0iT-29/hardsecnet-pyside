# First Run Guide

This is the document a new developer should start with.

## What You Are Looking At

HardSecNet is not just one app.

There are four moving parts:

1. desktop operator app
2. control plane backend
3. device agent
4. browser dashboard

You can work on one surface in isolation, but the full product story involves all four.

## What To Run First

If you only want to prove the repo works locally:

1. create and activate the Python venv
2. install the Python dependencies
3. run the tests
4. build the dashboard

Commands:

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
.\.venv\Scripts\python.exe -m pytest -q tests
```

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm install
npm run build
```

If those pass, the repo is in a basically healthy development state.

## What To Run For A Full Local Demo

### Start the control plane

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_CP_DATABASE_URL = "sqlite:///./runtime/control_plane.db"
$env:HARDSECNET_CP_ARTIFACTS_DIR = ".\\runtime\\control_plane_artifacts"
.\.venv\Scripts\python.exe -m uvicorn services.control_plane.app.main:app --reload
```

### Start the dashboard

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside\web\dashboard
npm run dev
```

### Start a device agent

Windows example:

```powershell
cd E:\T\hardsecnet\hardsecnet-pyside
.\.venv\Scripts\Activate.ps1
$env:HARDSECNET_AGENT_URL = "http://127.0.0.1:8000"
$env:HARDSECNET_AGENT_DEVICE_ID = "agent-01"
$env:HARDSECNET_AGENT_DEVICE_NAME = "Agent 01"
$env:HARDSECNET_AGENT_OS = "windows"
.\.venv\Scripts\python.exe -m services.device_agent.hardsecnet_device_agent.main
```

At that point the dashboard should be able to show:

- a device
- heartbeats
- jobs once created
- reports once results are submitted

## Where New Users Usually Get Confused

### 1. “The dashboard is blank”

Usually one of these:

- control plane is not running
- browser is blocked by API/CORS mismatch
- there are no devices/jobs/reports yet

The dashboard now shows better loading and empty states, but this is still the first thing to check.

### 2. “Why are there benchmark exports and runtime imports?”

Two separate concepts:

- `runtime/imports/` is the runtime ingestion path
- `src/hardsecnet_pyside/data/benchmark_exports/` is durable extracted source owned by the project

The second one is what removes dependence on the original PDF at runtime.

### 3. “Are the generated scripts safe to run?”

Not automatically.

They are benchmark-derived candidates. Some are close to usable. Some are still policy templates.

Use review and validation before treating them as production hardening scripts.

## Files Worth Reading Early

- [README.md](/E:/T/hardsecnet/hardsecnet-pyside/README.md)
- [ARCHITECTURE_GUIDE.md](/E:/T/hardsecnet/hardsecnet-pyside/docs/ARCHITECTURE_GUIDE.md)
- [CIS_BENCHMARK_ENGINE.md](/E:/T/hardsecnet/hardsecnet-pyside/docs/CIS_BENCHMARK_ENGINE.md)

## Good First Tasks For A New Developer

- improve a dashboard screen
- extend control-plane endpoints
- validate a batch of Ubuntu generated scripts
- convert a batch of Windows policy templates into real PowerShell logic
- add tests around benchmark import edge cases
