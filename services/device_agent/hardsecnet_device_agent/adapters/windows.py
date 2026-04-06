from __future__ import annotations

from pathlib import Path

from .base import AdapterResult, BaseAdapter


class WindowsAdapter(BaseAdapter):
    def execute(self, action: str, payload: dict) -> AdapterResult:
        scripts_root = self.workspace_root / "sw" / "hardsecnet-windows" / "scripts"
        command_map = {
            "remote-audit": scripts_root / "Auditor.ps1",
            "remote-harden": scripts_root / "Hardener.ps1",
            "remote-compare": scripts_root / "Comparison.ps1",
            "remote-snapshot": scripts_root / "Snapshot.ps1",
        }
        target = Path(payload.get("script_path", command_map.get(action, scripts_root / "Auditor.ps1")))
        if not target.exists():
            return AdapterResult(
                status="failed",
                summary=f"Windows script not found for action {action}",
                artifacts=[],
                details={"error": f"Missing script: {target}"},
            )
        completed = self._run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(target)], target.parent)
        status = "completed" if completed.returncode == 0 else "failed"
        return AdapterResult(
            status=status,
            summary=completed.stdout.strip() or completed.stderr.strip() or f"{action} finished",
            artifacts=[],
            details={"stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode},
        )
