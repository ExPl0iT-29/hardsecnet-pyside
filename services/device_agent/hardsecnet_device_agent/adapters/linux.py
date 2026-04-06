from __future__ import annotations

from pathlib import Path

from .base import AdapterResult, BaseAdapter


class LinuxAdapter(BaseAdapter):
    def execute(self, action: str, payload: dict) -> AdapterResult:
        module = payload.get("module", "Networking")
        scripts_root = self.workspace_root / "sw" / "HardSecNetLinux"
        module_root = scripts_root / module
        command_map = {
            "remote-audit": module_root / "audit.sh",
            "remote-harden": module_root / "harden.sh",
            "remote-unharden": module_root / "unharden.sh",
        }
        target = Path(payload.get("script_path", command_map.get(action, module_root / "audit.sh")))
        if not target.exists():
            return AdapterResult(
                status="failed",
                summary=f"Linux script not found for action {action}",
                artifacts=[],
                details={"error": f"Missing script: {target}"},
            )
        completed = self._run(["bash", str(target)], target.parent)
        status = "completed" if completed.returncode == 0 else "failed"
        return AdapterResult(
            status=status,
            summary=completed.stdout.strip() or completed.stderr.strip() or f"{action} finished",
            artifacts=[],
            details={"stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode},
        )
