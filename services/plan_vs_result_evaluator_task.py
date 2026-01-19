from datetime import datetime


class PlanVsResultEvaluatorTask:
    """
    Compara planes ejecutados con resultados reales.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        plans = cognitive.get("weekly_plans", [])
        metrics = cognitive.get("metrics", {}).get("daily", {})

        if not plans or not metrics:
            return None

        last_plan = plans[-1]
        if last_plan.get("completed"):
            return None

        # Resultado real: progreso reciente
        recent = list(metrics.values())[-5:]
        total_progress = sum(d.get("concepts_used", 0) for d in recent)

        evaluation = {
            "goal": last_plan.get("goal"),
            "evaluated_at": datetime.utcnow().isoformat(),
            "expected_focus": last_plan.get("focus"),
            "actual_progress": total_progress,
            "result": (
                "successful" if total_progress >= 5 else
                "weak" if total_progress > 0 else
                "failed"
            )
        }

        cognitive.setdefault("plan_result_evaluations", []).append(evaluation)

        # Marcar plan como completado si fue exitoso
        if evaluation["result"] == "successful":
            last_plan["completed"] = True

        self.memory.log_event(
            event="plan_vs_result_evaluated",
            summary=(
                f"Plan '{last_plan.get('goal')}' → "
                f"{evaluation['result']}"
            )
        )
        self.memory._persist()

        return evaluation