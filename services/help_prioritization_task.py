from datetime import datetime


class HelpPrioritizationTask:
    """
    Prioriza qué tipo de ayuda humana pedir.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        patterns = cognitive.get("error_patterns", [])
        evaluations = cognitive.get("plan_result_evaluations", [])

        priorities = []

        # Prioridad 1: errores persistentes
        for p in patterns:
            if p.get("active") and p.get("occurrences", 0) >= 5:
                priorities.append({
                    "type": "debugging_help",
                    "reason": f"Errores recurrentes del tipo {p.get('type')}",
                    "priority": 1
                })

        # Prioridad 2: planes fallidos
        for e in evaluations[-3:]:
            if e.get("result") == "failed":
                priorities.append({
                    "type": "strategy_review",
                    "reason": f"Plan fallido: {e.get('goal')}",
                    "priority": 2
                })

        if not priorities:
            return None

        priorities.sort(key=lambda x: x["priority"])

        guardian["help_priorities"] = {
            "generated_at": datetime.utcnow().isoformat(),
            "items": priorities
        }

        self.memory.log_event(
            event="help_prioritized",
            summary=f"Prioridades de ayuda definidas ({len(priorities)})"
        )
        self.memory._persist()

        return priorities