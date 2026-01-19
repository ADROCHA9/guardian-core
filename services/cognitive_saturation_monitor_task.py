from datetime import datetime, timedelta


class CognitiveSaturationMonitorTask:
    """
    Detecta saturación cognitiva prolongada y auto-pausa Guardian.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {}).get("daily", {})

        if len(metrics) < 3:
            return None

        last_days = list(metrics.values())[-3:]
        avg = sum(d.get("concepts_used", 0) for d in last_days) / len(last_days)

        if avg < 1:
            guardian["paused"] = True
            guardian["pause_reason"] = "saturación cognitiva prolongada"
            guardian["paused_at"] = datetime.utcnow().isoformat()

            self.memory.log_event(
                event="guardian_auto_paused",
                summary="Saturación cognitiva detectada. Guardian en pausa."
            )
            self.memory._persist()

            return "paused"

        return "ok"