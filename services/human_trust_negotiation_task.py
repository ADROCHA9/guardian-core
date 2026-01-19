from datetime import datetime


class HumanTrustNegotiationTask:
    """
    Ajusta el nivel de confianza de Guardian en humanos
    según resultados históricos.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        negotiations = cognitive.get("idea_negotiations", [])
        evaluations = cognitive.get("plan_result_evaluations", [])

        trust = guardian.get("human_trust_level", 0.5)  # 0.0 a 1.0

        # Analizar impacto de ideas humanas
        positive = 0
        negative = 0

        for n in negotiations[-5:]:
            if n.get("decision") == "accept":
                positive += 1
            elif n.get("decision") == "reject":
                negative += 1

        for e in evaluations[-5:]:
            if e.get("result") == "successful":
                positive += 1
            elif e.get("result") == "failed":
                negative += 1

        # Ajuste suave
        if positive > negative:
            trust = min(1.0, trust + 0.1)
        elif negative > positive:
            trust = max(0.0, trust - 0.1)

        guardian["human_trust_level"] = round(trust, 2)
        guardian["human_trust_updated_at"] = datetime.utcnow().isoformat()

        self.memory.log_event(
            event="human_trust_updated",
            summary=f"Nivel de confianza humana ajustado a {guardian['human_trust_level']}"
        )
        self.memory._persist()

        return guardian["human_trust_level"]