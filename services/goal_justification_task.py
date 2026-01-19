from datetime import datetime


class GoalJustificationTask:
    """
    Genera una justificación explícita del objetivo actual.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        intent = guardian.get("learning_intent")
        if not intent:
            return None

        metrics = cognitive.get("metrics", {}).get("daily", {})
        patterns = cognitive.get("error_patterns", [])
        heuristics = cognitive.get("error_heuristics", [])

        justification = {
            "goal": intent.get("goal"),
            "generated_at": datetime.utcnow().isoformat(),
            "reasons": []
        }

        # Evidencia por errores
        for p in patterns:
            if p.get("active") and p.get("type") in intent.get("goal", "").lower():
                justification["reasons"].append(
                    f"Patrón de error recurrente ({p.get('type')})"
                )

        # Evidencia por heurísticas
        if heuristics:
            justification["reasons"].append(
                f"{len(heuristics)} heurísticas activas influyen en este objetivo"
            )

        # Evidencia por progreso reciente
        if metrics:
            last = list(metrics.values())[-1]
            if last.get("concepts_used", 0) < 1:
                justification["reasons"].append(
                    "Progreso reciente bajo, se requiere refuerzo"
                )

        guardian["learning_intent_justification"] = justification

        self.memory.log_event(
            event="goal_justified",
            summary=f"Objetivo justificado: {intent.get('goal')}"
        )
        self.memory._persist()

        return justification