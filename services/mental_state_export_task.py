import json
import os
from datetime import datetime


class MentalStateExportTask:
    """
    Exporta el estado mental actual de Guardian a un archivo JSON.
    """

    def __init__(self, memory, export_dir="exports"):
        self.memory = memory
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    def run(self) -> str:
        snapshot = {
            "exported_at": datetime.utcnow().isoformat(),
            "guardian_self": self.memory._memory.get("guardian_self", {}),
            "cognitive_memory": self.memory._memory.get("cognitive_memory", {})
        }

        filename = f"guardian_mental_state_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(self.export_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)

        self.memory.log_event(
            event="mental_state_exported",
            summary=f"Estado mental exportado a {filename}"
        )
        self.memory._persist()

        return path