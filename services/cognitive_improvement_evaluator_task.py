from datetime import datetime


class CognitiveImprovementEvaluatorTask:
    """
    Define y evalúa si Guardian está mejorando realmente.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        metrics = cognitive.get("metrics", {}).get("daily", {})
        if len(metrics) < 5:
            return None

        last = list(metrics.values())[-5:]
        avg_progress = sum(d.get("concepts_used", 0) for d in last) / len(last)

        memory_size = len(str(cognitive))
        errors = len(cognitive.get("error_patterns", []))
        dependency = guardian.get("human_dependency", 0.5)

        improved = (
            avg_progress >= 1 and
            errors <= 5 and
            dependency <= 0.5
        )

        result = {
            "evaluated_at": datetime.utcnow().isoformat(),
            "avg_progress": avg_progress,
            "memory_size": memory_size,
            "error_count": errors,
            "human_dependency": dependency,
            "improved": improved
        }

        guardian["last_improvement_evaluation"] = result
        self.memory._persist()
        return result