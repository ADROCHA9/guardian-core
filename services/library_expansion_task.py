from datetime import datetime


class HumanDependencyDecayTask:
    """
    Reduce dependencia humana cuando Guardian progresa sin ayuda.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        metrics = cognitive.get("metrics", {}).get("daily", {})
        if len(metrics) < 5:
            return None

        last_days = list(metrics.values())[-5:]
        avg = sum(d.get("concepts_used", 0) for d in last_days) / len(last_days)

        dependency = guardian.get("human_dependency", 0.5)

        if avg >= 2:
            dependency = max(0.0, dependency - 0.05)

        guardian["human_dependency"] = round(dependency, 2)

        self.memory.log_event(
            event="human_dependency_updated",
            summary=f"Dependencia humana ajustada a {dependency}"
        )
        self.memory._persist()

        return dependency