from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AdapterResult:
    status: str
    summary: str
    artifacts: list[str]
    details: dict


class BaseAdapter:
    def __init__(self, workspace_root: Path) -> None:
        self.workspace_root = workspace_root

    def execute(self, action: str, payload: dict) -> AdapterResult:
        raise NotImplementedError

    def _run(self, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=300, check=False)
