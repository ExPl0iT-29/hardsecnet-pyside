from __future__ import annotations

import os
import platform
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AgentConfig:
    control_plane_url: str = os.getenv("HARDSECNET_AGENT_URL", "http://127.0.0.1:8000")
    username: str = os.getenv("HARDSECNET_AGENT_ADMIN", "admin")
    password: str = os.getenv("HARDSECNET_AGENT_PASSWORD", "admin")
    enrollment_token: str = os.getenv("HARDSECNET_AGENT_ENROLLMENT_TOKEN", "")
    device_id: str = os.getenv("HARDSECNET_AGENT_DEVICE_ID", platform.node().lower() or "agent-device")
    device_name: str = os.getenv("HARDSECNET_AGENT_DEVICE_NAME", platform.node() or "Agent Device")
    hostname: str = os.getenv("HARDSECNET_AGENT_HOSTNAME", platform.node() or "localhost")
    os_family: str = os.getenv(
        "HARDSECNET_AGENT_OS",
        "windows" if platform.system().lower().startswith("win") else "linux",
    )
    workspace_root: Path = Path(os.getenv("HARDSECNET_WORKSPACE_ROOT", "E:/T/hardsecnet"))
    state_dir: Path = field(default_factory=lambda: Path("./runtime/device_agent"))

    def ensure(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
