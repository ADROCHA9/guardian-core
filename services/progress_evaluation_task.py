from datetime import datetime


class ProgressEvaluationTask:
    """
    Calcula progreso real del Guardian.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        metrics = cognitive.setdefault("metrics", {})
        concepts = cognitive.get("concepts", {})

        today = datetime.utcnow().date().isoformat()
        daily = metrics.setdefault("daily", {})

        daily[today] = {
            "concepts_used": sum(c["uses"] for c in concepts.values()),
            "concepts_dominated": len([c for c in concepts.values() if c["dominated"]]),
            "fragile": len([c for c in concepts.values() if c["fragile"]])
        }

        self.memory._persist()