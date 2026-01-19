import hashlib
import json
from datetime import datetime


class MindVersioningTask:
    """
    Versiona el estado cognitivo como hitos mentales.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        snapshot = {
            "concepts": list(cognitive.get("concepts", {}).keys()),
            "error_patterns": len(cognitive.get("error_patterns", [])),
            "autonomy": guardian.get("autonomy_mode"),
            "limits": guardian.get("ethical_limits"),
            "dependency": guardian.get("human_dependency")
        }

        raw = json.dumps(snapshot, sort_keys=True).encode()
        signature = hashlib.sha256(raw).hexdigest()

        version = {
            "created_at": datetime.utcnow().isoformat(),
            "signature": signature,
            "snapshot": snapshot
        }

        guardian.setdefault("mind_versions", []).append(version)
        self.memory._persist()
        return version