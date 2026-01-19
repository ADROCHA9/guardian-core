from datetime import datetime


class IdeaCriticalEvaluatorTask:
    """
    Evalúa ideas y decide si son:
    - válidas
    - riesgosas
    - inútiles
    """

    def __init__(self, memory):
        self.memory = memory

    def evaluate(self, idea_text: str, source: str = "human"):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        heuristics = cognitive.get("error_heuristics", [])
        dependencies = cognitive.get("concept_dependencies", [])

        decision = {
            "idea": idea_text,
            "source": source,
            "decision": "accept",
            "reason": "No se detectaron conflictos.",
            "timestamp": datetime.utcnow().isoformat()
        }

        # ❌ Heurísticas contradictorias
        for h in heuristics:
            if h.get("active") and h.get("when_error_type") in idea_text.lower():
                decision.update({
                    "decision": "reject",
                    "reason": "Contradice heurísticas aprendidas."
                })

        # ❌ Dependencias no cumplidas
        for d in dependencies:
            if d.get("blocked") and d.get("concept") in idea_text.lower():
                decision.update({
                    "decision": "reject",
                    "reason": "Dependencias conceptuales no satisfechas."
                })

        cognitive.setdefault("idea_evaluations", []).append(decision)

        self.memory.log_event(
            event="idea_evaluated",
            summary=f"Idea '{idea_text}' → {decision['decision']}"
        )
        self.memory._persist()

        return decision