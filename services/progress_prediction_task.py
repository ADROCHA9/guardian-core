from datetime import datetime, timedelta


class ProgressPredictionTask:
    """
    Predice progreso futuro basado en métricas reales.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {}).get("daily", {})

        if len(metrics) < 7:
            return None

        last_days = list(metrics.values())[-7:]
        avg = sum(d.get("concepts_used", 0) for d in last_days) / len(last_days)

        prediction = {
            "predicted_at": datetime.utcnow().isoformat(),
            "daily_average": avg,
            "in_7_days": avg * 7,
            "in_30_days": avg * 30
        }

        cognitive["progress_prediction"] = prediction

        self.memory.log_event(
            event="progress_predicted",
            summary=f"Predicción: +{int(prediction['in_7_days'])} conceptos en 7 días"
        )
        self.memory._persist()

        return prediction