from datetime import datetime


class StrategyHistoryComparisonTask:
    """
    Compara la efectividad histórica de estrategias usadas.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        evaluations = cognitive.get("plan_result_evaluations", [])

        if len(evaluations) < 2:
            return None

        summary = {}
        for e in evaluations:
            goal = e.get("goal")
            result = e.get("result")
            summary.setdefault(goal, {"successful": 0, "weak": 0, "failed": 0})
            summary[goal][result] += 1

        comparison = {
            "generated_at": datetime.utcnow().isoformat(),
            "strategies": summary
        }

        cognitive["strategy_history_comparison"] = comparison

        self.memory.log_event(
            event="strategy_history_compared",
            summary="Comparación histórica de estrategias actualizada"
        )
        self.memory._persist()

        return comparison