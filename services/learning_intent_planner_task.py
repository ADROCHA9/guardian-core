import time


class LearningIntentPlannerTask:
    """
    Mantiene continuidad cognitiva.
    """

    def __init__(self, memory):
        self.memory = memory

    def set_intent(self, goal: str, reason: str):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        guardian["learning_intent"] = {
            "goal": goal,
            "reason": reason,
            "since": time.time()
        }
        self.memory._persist()

    def get_intent(self):
        return self.memory._memory.get("guardian_self", {}).get("learning_intent")