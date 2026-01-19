from datetime import datetime
from typing import Dict, List

MAX_DECISIONS = 80
MAX_GUI_HINTS = 50
MAX_RAW_IDEAS = 60
DECAY_SECONDS = 60 * 60  # 1h


class CognitiveLearningLayer:
    """
    Aprendizaje explícito + limpieza cognitiva.
    Server-safe, sin fuga de memoria.
    """

    def __init__(self, memory):
        self.memory = memory
        self._ensure_structures()

    def _ensure_structures(self):
        if not hasattr(self.memory, "_memory"):
            return

        cm = self.memory._memory.setdefault("cognitive_memory", {})
        cm.setdefault("decisions", [])
        cm.setdefault("preferences", {})
        cm.setdefault("patterns", [])
        cm.setdefault("gui_hints", [])
        cm.setdefault("raw_ideas", [])

    def process(self, core_result: Dict, human_input: str | None) -> Dict:
        cm = self.memory._memory.get("cognitive_memory", {})

        if human_input and core_result.get("mode") == "learning":
            self._record_decision(human_input, "human_interaction")

        ideas = core_result.get("ideas", [])
        now = datetime.utcnow().timestamp()

        for idea in ideas:
            cm["raw_ideas"].append({
                "idea": idea,
                "timestamp": now
            })

        self._cleanup()
        self.memory._persist()
        return core_result

    def _record_decision(self, text: str, reason: str):
        cm = self.memory._memory["cognitive_memory"]
        cm["decisions"].append({
            "input": text,
            "reason": reason,
            "timestamp": datetime.utcnow().timestamp()
        })

    def _cleanup(self):
        cm = self.memory._memory["cognitive_memory"]
        now = datetime.utcnow().timestamp()

        cm["decisions"] = cm["decisions"][-MAX_DECISIONS:]
        cm["gui_hints"] = cm["gui_hints"][-MAX_GUI_HINTS:]

        cm["raw_ideas"] = [
            i for i in cm["raw_ideas"]
            if now - i["timestamp"] < DECAY_SECONDS
        ][-MAX_RAW_IDEAS:]
