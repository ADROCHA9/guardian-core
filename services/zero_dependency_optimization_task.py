from datetime import datetime


class ZeroDependencyOptimizationTask:
    """
    Optimiza el comportamiento de Guardian para minimizar
    y eventualmente eliminar dependencia humana.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        metrics = cognitive.get("metrics", {}).get("daily", {})
        dependency = guardian.get("human_dependency", 0.5)

        if len(metrics) < 10:
            return None

        last_days = list(metrics.values())[-10:]
        avg_progress = sum(
            d.get("concepts_used", 0) for d in last_days
        ) / len(last_days)

        # Señal fuerte de autonomía
        if avg_progress >= 2 and dependency <= 0.2:
            guardian["autonomy_mode"] = {
                "enabled": True,
                "since": datetime.utcnow().isoformat(),
                "reason": "Progreso autónomo sostenido"
            }

            self.memory.log_event(
                event="autonomy_mode_enabled",
                summary="Guardian entra en modo de autonomía casi total"
            )
            self.memory._persist()

            return "autonomy_enabled"

        return None