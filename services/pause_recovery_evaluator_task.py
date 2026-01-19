from datetime import datetime


class PauseRecoveryEvaluatorTask:
    """
    Decide cuándo Guardian puede salir solo de una pausa.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        if not guardian.get("paused"):
            return None

        metrics = cognitive.get("metrics", {}).get("daily", {})
        if len(metrics) < 3:
            return None

        last_days = list(metrics.values())[-3:]
        avg = sum(d.get("concepts_used", 0) for d in last_days) / len(last_days)

        # Señal de recuperación
        if avg >= 1:
            guardian["paused"] = False
            guardian["resumed_at"] = datetime.utcnow().isoformat()
            guardian["pause_reason"] = None

            self.memory.log_event(
                event="guardian_auto_resumed",
                summary="Guardian se reanuda tras detectar recuperación cognitiva"
            )
            self.memory._persist()

            return "resumed"

        return "still_paused"