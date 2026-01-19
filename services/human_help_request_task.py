from datetime import datetime


class HumanHelpRequestTask:
    """
    Decide cuándo Guardian debe pedir ayuda humana.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        evaluations = cognitive.get("plan_result_evaluations", [])
        adjustments = cognitive.get("strategy_adjustments", [])

        # Señales de bloqueo
        recent_evals = evaluations[-3:]
        failures = [e for e in recent_evals if e.get("result") == "failed"]

        if len(failures) >= 2 and len(adjustments) >= 2:
            request = {
                "requested_at": datetime.utcnow().isoformat(),
                "reason": (
                    "Múltiples fallos consecutivos y cambios de estrategia "
                    "sin mejora significativa."
                ),
                "status": "pending"
            }

            guardian["human_help_requested"] = request

            self.memory.log_event(
                event="human_help_requested",
                summary="Guardian solicita ayuda humana"
            )
            self.memory._persist()

            return request

        return None