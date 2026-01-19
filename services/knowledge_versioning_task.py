import hashlib
import json
from datetime import datetime


class KnowledgeVersioningTask:
    """
    Versiona el conocimiento por hitos reales.
    """

    def __init__(self, memory):
        self.memory = memory

    def maybe_create_version(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        concepts = cognitive.get("concepts", {})
        level_sum = sum(c.get("level", 0) for c in concepts.values())

        last_level_sum = guardian.get("last_version_level_sum", 0)

        # Crear versión solo si hay avance REAL
        if level_sum < last_level_sum + 5:
            return None

        payload = json.dumps(
            cognitive,
            sort_keys=True,
            ensure_ascii=False
        ).encode("utf-8")

        version = {
            "created_at": datetime.utcnow().isoformat(),
            "level_sum": level_sum,
            "hash": hashlib.sha256(payload).hexdigest()
        }

        guardian.setdefault("knowledge_versions", []).append(version)
        guardian["last_version_level_sum"] = level_sum

        self.memory.log_event(
            event="knowledge_version_created",
            summary=f"Nuevo hito cognitivo (nivel total {level_sum})"
        )
        self.memory._persist()

        return version