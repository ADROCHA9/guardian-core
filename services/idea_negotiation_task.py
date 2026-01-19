from datetime import datetime


class IdeaNegotiationTask:
    """
    Negocia ideas entre humano y Guardian.
    """

    def __init__(self, memory):
        self.memory = memory

    def negotiate(self, human_idea: str):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        current_goal = guardian.get("learning_intent", {})
        heuristics = cognitive.get("error_heuristics", [])

        decision = {
            "human_idea": human_idea,
            "decision": "accept",
            "final_goal": human_idea,
            "reason": "Compatible con estado actual",
            "timestamp": datetime.utcnow().isoformat()
        }

        # Conflicto con heurísticas
        for h in heuristics:
            if h.get("active") and h.get("when_error_type") in human_idea.lower():
                decision.update({
                    "decision": "modify",
                    "final_goal": current_goal.get("goal", human_idea),
                    "reason": "Conflicto con heurísticas internas"
                })

        guardian["learning_intent"] = {
            "goal": decision["final_goal"],
            "source": "negotiated",
            "timestamp": decision["timestamp"]
        }

        cognitive.setdefault("idea_negotiations", []).append(decision)

        self.memory.log_event(
            event="idea_negotiated",
            summary=f"Idea negociada → {decision['decision']}"
        )
        self.memory._persist()

        return decision