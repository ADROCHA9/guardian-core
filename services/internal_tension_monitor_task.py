import time

class InternalTensionMonitorTask:
    """
    Genera tensión cognitiva cuando no hay cambio real.
    """

    MAX_STATIC_TIME = 60 * 60  # 1 horas sin cambio real

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})

        last_change = cognitive.get("last_model_change_ts", 0)
        now = time.time()

        tension = guardian.get("internal_tension", 0)

        if now - last_change > self.MAX_STATIC_TIME:
            tension += 1
        else:
            tension = max(0, tension - 1)

        guardian["internal_tension"] = tension

        return tension