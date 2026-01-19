from datetime import datetime


class StrategyChangeExplanationTask:
    """
    Explica por qué Guardian decidió cambiar de estrategia.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        adjustments = cognitive.get("strategy_adjustments", [])
        evaluations = cognitive.get("plan_result_evaluations", [])

        if not adjustments or not evaluations:
            return None

        last_adjustment = adjustments[-1]
        last_eval = evaluations[-1]

        explanation = {
            "goal": last_adjustment.get("original_goal"),
            "changed_at": last_adjustment.get("proposed_at"),
            "explanation": (
                f"Cambié de estrategia porque el plan anterior fue "
                f"{last_eval.get('result')}. "
                f"El progreso real fue "
                f"{last_eval.get('actual_progress')} conceptos, "
                f"lo cual es insuficiente para el objetivo planteado."
            ),
            "timestamp": datetime.utcnow().isoformat()
        }

        cognitive.setdefault("strategy_change_explanations", []).append(explanation)

        self.memory.log_event(
            event="strategy_change_explained",
            summary=f"Estrategia explicada para {explanation['goal']}"
        )
        self.memory._persist()

        return explanation