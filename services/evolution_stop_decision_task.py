from datetime import datetime


class EvolutionStopDecisionTask:
    """
    Decide cuándo Guardian debe detener su evolución activa.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        evaluation = guardian.get("last_improvement_evaluation")

        if not evaluation:
            return None

        if not evaluation.get("improved"):
            guardian["evolution_paused"] = {
                "paused_at": datetime.utcnow().isoformat(),
                "reason": "No se detecta mejora real sostenida"
            }
            self.memory._persist()
            return guardian["evolution_paused"]

        return None