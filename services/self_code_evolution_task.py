from datetime import datetime


class SelfCodeEvolutionTask:
    """
    Permite auto-modificación SOLO si el nivel cognitivo lo permite.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        level = guardian.get("module_evolution", {}).get("tier")

        if level not in ("advanced",):
            return None  # bloqueado por diseño

        evolution = {
            "attempted_at": datetime.utcnow().isoformat(),
            "action": "proposed_refactor",
            "status": "proposal_only"
        }

        guardian.setdefault("self_code_actions", []).append(evolution)
        self.memory._persist()
        return evolution