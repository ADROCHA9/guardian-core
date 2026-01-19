from datetime import datetime


class PlanHumanExplanationTask:
    """
    Genera explicaciones en lenguaje humano de los planes activos.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        plans = cognitive.get("weekly_plans", [])
        if not plans:
            return None

        active_plan = plans[-1]
        if active_plan.get("completed"):
            return None

        explanation = (
            f"Estoy trabajando en el objetivo '{active_plan.get('goal')}' "
            f"porque detecté que es importante consolidarlo ahora. "
            f"Planeo enfocarme durante esta semana para mejorar estabilidad "
            f"y reducir errores relacionados."
        )

        guardian["current_plan_explanation"] = {
            "text": explanation,
            "generated_at": datetime.utcnow().isoformat()
        }

        self.memory.log_event(
            event="plan_explained_humanly",
            summary=f"Plan explicado: {active_plan.get('goal')}"
        )
        self.memory._persist()

        return explanation