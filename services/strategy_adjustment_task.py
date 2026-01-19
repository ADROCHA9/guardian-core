from datetime import datetime


class StrategyAdjustmentTask:
    """
    Propone cambios de estrategia cuando los planes no funcionan bien.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        evaluations = cognitive.get("plan_result_evaluations", [])
        if not evaluations:
            return None

        last_eval = evaluations[-1]
        if last_eval.get("result") == "successful":
            return None

        suggestion = {
            "original_goal": last_eval.get("goal"),
            "proposed_change": "",
            "reason": "",
            "proposed_at": datetime.utcnow().isoformat()
        }

        if last_eval["result"] == "failed":
            suggestion["proposed_change"] = (
                "Reducir complejidad y volver a conceptos base relacionados."
            )
            suggestion["reason"] = "El plan no produjo progreso medible."
        else:  # weak
            suggestion["proposed_change"] = (
                "Cambiar enfoque a micro-tests más pequeños y específicos."
            )
            suggestion["reason"] = "El progreso fue menor al esperado."

        cognitive.setdefault("strategy_adjustments", []).append(suggestion)

        self.memory.log_event(
            event="strategy_adjustment_proposed",
            summary=f"Cambio de estrategia propuesto para '{suggestion['original_goal']}'"
        )
        self.memory._persist()

        return suggestion