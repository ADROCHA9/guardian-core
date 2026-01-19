from datetime import datetime


class PlanSelfEvaluationTask:
    """
    Guardian evalúa si sus propios planes están funcionando.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        plans = cognitive.get("proposed_plans", [])
        metrics = cognitive.get("metrics", {}).get("daily", {})

        if not plans or not metrics:
            return None

        latest_metric = list(metrics.values())[-1]
        score = latest_metric.get("concepts_used", 0)

        evaluations = cognitive.setdefault("plan_evaluations", [])

        for plan in plans[-3:]:
            effectiveness = "neutral"
            if score > 0:
                effectiveness = "positive"
            elif score == 0:
                effectiveness = "ineffective"

            evaluations.append({
                "goal": plan.get("goal"),
                "evaluated_at": datetime.utcnow().isoformat(),
                "effectiveness": effectiveness,
                "reason": (
                    "Incremento de conceptos detectado"
                    if effectiveness == "positive"
                    else "Sin impacto medible aún"
                )
            })

        self.memory.log_event(
            event="plans_self_evaluated",
            summary=f"{len(plans[-3:])} planes evaluados por Guardian"
        )
        self.memory._persist()

        return evaluations