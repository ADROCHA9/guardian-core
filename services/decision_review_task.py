class DecisionReviewTask:
    """
    Compara decisiones pasadas y ajusta criterio.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self) -> dict:
        history = self.memory.get("evolution_decisions", [])
        insights = []

        for d in history[-5:]:
            if not d.get("priorities"):
                insights.append("Decisión sin prioridades claras")

        return {
            "reviewed": len(history),
            "insights": insights
        }