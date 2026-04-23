import json
from dataclasses import is_dataclass, asdict
from PySide6.QtCore import QObject, Slot, Signal

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "isoformat"):
            return obj.isoformat()
        return super().default(obj)

class WebBridge(QObject):
    snapshotUpdated = Signal(str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    @Slot(result=str)
    def getDashboardSnapshot(self):
        try:
            snapshot = self.controller.dashboard_snapshot()
            return json.dumps(snapshot, cls=CustomJSONEncoder)
        except Exception as e:
            return json.dumps({"error": str(e)})

    @Slot(str, result=str)
    def runProfile(self, profile_id):
        try:
            run = self.controller.run_profile(profile_id)
            self.refreshSnapshot()
            return json.dumps({"success": True, "run_id": run.id})
        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    @Slot()
    def refreshSnapshot(self):
        try:
            snapshot = self.controller.dashboard_snapshot()
            payload = json.dumps(snapshot, cls=CustomJSONEncoder)
            self.snapshotUpdated.emit(payload)
        except Exception as e:
            self.snapshotUpdated.emit(json.dumps({"error": str(e)}))
