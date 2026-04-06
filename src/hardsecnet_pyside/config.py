from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppPaths:
    project_root: Path
    workspace_root: Path
    runtime_dir: Path
    artifacts_dir: Path
    reports_dir: Path
    logs_dir: Path
    imports_dir: Path
    database_path: Path
    windows_repo: Path
    linux_repo: Path

    @classmethod
    def discover(cls, project_root: Path) -> "AppPaths":
        workspace_root = project_root.parent
        runtime_dir = project_root / "runtime"
        return cls(
            project_root=project_root,
            workspace_root=workspace_root,
            runtime_dir=runtime_dir,
            artifacts_dir=runtime_dir / "artifacts",
            reports_dir=runtime_dir / "reports",
            logs_dir=runtime_dir / "logs",
            imports_dir=runtime_dir / "imports",
            database_path=runtime_dir / "hardsecnet.db",
            windows_repo=workspace_root / "sw" / "hardsecnet-windows",
            linux_repo=workspace_root / "sw" / "HardSecNetLinux",
        )

    def ensure(self) -> None:
        for path in (
            self.runtime_dir,
            self.artifacts_dir,
            self.reports_dir,
            self.logs_dir,
            self.imports_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


@dataclass(slots=True)
class AISettings:
    mode: str = "hybrid"
    local_provider: str = "ollama"
    local_endpoint: str = "http://127.0.0.1:11434/api/generate"
    local_model: str = "phi3"
    cloud_endpoint: str = ""
    cloud_api_key: str = ""
    cloud_model: str = ""

    @classmethod
    def from_env(cls) -> "AISettings":
        return cls(
            mode=os.getenv("HARDSECNET_AI_MODE", "hybrid"),
            local_provider=os.getenv("HARDSECNET_LOCAL_PROVIDER", "ollama"),
            local_endpoint=os.getenv(
                "HARDSECNET_LOCAL_ENDPOINT", "http://127.0.0.1:11434/api/generate"
            ),
            local_model=os.getenv("HARDSECNET_LOCAL_MODEL", "phi3"),
            cloud_endpoint=os.getenv("HARDSECNET_CLOUD_ENDPOINT", ""),
            cloud_api_key=os.getenv("HARDSECNET_CLOUD_API_KEY", ""),
            cloud_model=os.getenv("HARDSECNET_CLOUD_MODEL", ""),
        )


@dataclass(slots=True)
class ControlPlaneSettings:
    base_url: str = ""
    username: str = "admin"
    password: str = "admin"

    @classmethod
    def from_env(cls) -> "ControlPlaneSettings":
        return cls(
            base_url=os.getenv("HARDSECNET_CONTROL_PLANE_URL", "").rstrip("/"),
            username=os.getenv("HARDSECNET_CONTROL_PLANE_USER", "admin"),
            password=os.getenv("HARDSECNET_CONTROL_PLANE_PASSWORD", "admin"),
        )
