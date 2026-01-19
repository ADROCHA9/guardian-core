class ExperimentalMetaDesignerTask:
    """
    Nivel 3: propone rediseños cognitivos SIN ejecutar.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.get("guardian_self", {})
        if guardian.get("cognitive_level", 0) < 3:
            return None

        cognitive = self.memory._memory.setdefault("cognitive_memory", {})

        proposal = {
            "type": "structural_proposal",
            "idea": "Reducir frecuencia de exploración y aumentar evaluación",
            "reason": "Alta tasa de hipótesis con bajo ratio de cambio",
            "evidence": {
                "hypotheses": len(cognitive.get("internal_hypotheses", [])),
                "changes": len(cognitive.get("autobiography", []))
            }
        }

        cognitive.setdefault("experimental_proposals", []).append(proposal)
        return proposal