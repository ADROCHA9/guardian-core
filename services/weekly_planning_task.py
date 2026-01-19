from datetime import datetime, timedelta


class WeeklyPlanningTask:
    """
    Planificación cognitiva a nivel semanal.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        current_intent = guardian.get("learning_intent")
        if not current_intent:
            return None

        plans = cognitive.setdefault("weekly_plans", [])

        # Evitar duplicar plan activo
        if plans and not plans[-1].get("completed"):
            return plans[-1]

        plan = {
            "goal": current_intent.get("goal"),
            "created_at": datetime.utcnow().isoformat(),
            "expected_end": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "focus": "consolidation",
            "completed": False
        }

        plans.append(plan)

        self.memory.log_event(
            event="weekly_plan_created",
            summary=f"Plan semanal creado para: {plan['goal']}"
        )
        self.memory._persist()

        return plan