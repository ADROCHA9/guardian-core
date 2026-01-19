from statistics import mean


class AdaptiveIntelligence:
    """
    Motor adaptativo del Guardian.
    Aprende de decisiones pasadas, evalúa riesgo y
    propone ajustes de prioridad.
    """

    def __init__(self, memory):
        self.memory = memory

    # =================================================
    # APRENDIZAJE DE DECISIONES
    # =================================================
    def learn_from_decisions(self):
        """
        Analiza decisiones humanas pasadas para extraer patrones.
        """
        decisions = self.memory.get("decision_log", [])
        if not decisions:
            return {}

        stats = {}
        for d in decisions:
            pid = d.get("proposal_id")
            stats.setdefault(pid, 0)
            stats[pid] += 1

        return {
            "total_decisions": len(decisions),
            "decisions_per_proposal": stats
        }

    # =================================================
    # RIESGO CUANTITATIVO
    # =================================================
    def evaluate_risk(self, proposal):
        """
        Calcula un score de riesgo (0–1).
        """
        risk = 0.0

        if proposal.get("type") == "new_module":
            risk += 0.4
        if proposal.get("type") == "refactor":
            risk += 0.2
        if proposal.get("priority") == 1:
            risk += 0.2
        if proposal.get("depends_on"):
            risk += 0.1 * len(proposal.get("depends_on"))

        return min(risk, 1.0)

    # =================================================
    # AUTO-AJUSTE DE PRIORIDADES (PROPUESTA)
    # =================================================
    def propose_priority_adjustments(self):
        """
        Sugiere ajustes de prioridad basados en riesgo y experiencia pasada.
        """
        proposals = self.memory.get("proposed_connections", [])
        suggestions = []

        risks = {
            p["id"]: self.evaluate_risk(p)
            for p in proposals
        }

        avg_risk = mean(risks.values()) if risks else 0

        for p in proposals:
            pid = p["id"]
            risk = risks.get(pid, 0)
            current = p.get("priority")

            if current is None:
                continue

            if risk > avg_risk and current < 5:
                suggestions.append({
                    "proposal_id": pid,
                    "current_priority": current,
                    "suggested_priority": current + 1,
                    "reason": "Riesgo superior al promedio"
                })

        return suggestions