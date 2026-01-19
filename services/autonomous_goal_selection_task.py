from datetime import datetime


class AutonomousGoalSelectionTask:
    """
    Guardian selecciona sus propios objetivos de aprendizaje.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        concepts = cognitive.get("concepts", {})
        heuristics = cognitive.get("error_heuristics", [])
        patterns = cognitive.get("error_patterns", [])

        # Prioridad 1: errores activos frecuentes
        active_patterns = [
            p for p in patterns if p.get("active") and p.get("occurrences", 0) >= 3
        ]
        if active_patterns:
            target = active_patterns[0]["type"]
            goal = f"Reducir errores del tipo {target}"
            reason = "Patrón de error recurrente detectado"
        else:
            # Prioridad 2: conceptos frágiles
            fragile = [
                name for name, c in concepts.items()
                if c.get("level", 0) > 0 and c.get("stability", 1) < 0.5
            ]
            if fragile:
                goal = f"Reforzar concepto {fragile[0]}"
                reason = "Concepto frágil detectado"
            else:
                return None

        selected = {
            "goal": goal,
            "reason": reason,
            "selected_at": datetime.utcnow().isoformat(),
            "source": "autonomous"
        }

        guardian["learning_intent"] = selected

        self.memory.log_event(
            event="autonomous_goal_selected",
            summary=f"Objetivo elegido: {goal}"
        )
        self.memory._persist()

        return selected
