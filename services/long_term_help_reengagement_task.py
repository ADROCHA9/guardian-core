from datetime import datetime, timedelta


class LongTermHelpReengagementTask:
    """
    Decide cuándo Guardian debe volver a pedir ayuda humana
    tras un período prolongado de autonomía.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        autonomy = guardian.get("autonomy_mode")
        if not autonomy or not autonomy.get("enabled"):
            return None

        metrics = cognitive.get("metrics", {}).get("daily", {})
        if len(metrics) < 14:
            return None

        last_days = list(metrics.values())[-14:]
        avg_progress = sum(
            d.get("concepts_used", 0) for d in last_days
        ) / len(last_days)

        # Señal clara de estancamiento prolongado
        if avg_progress < 0.5:
            guardian["autonomy_mode"]["enabled"] = False
            guardian["autonomy_mode"]["disabled_at"] = datetime.utcnow().isoformat()
            guardian["autonomy_mode"]["reason"] = "Estancamiento prolongado"

            self.memory.log_event(
                event="autonomy_suspended_for_help",
                summary="Guardian reabre ayuda humana por estancamiento prolongado"
            )
            self.memory._persist()

            return "help_reengaged"

        return None