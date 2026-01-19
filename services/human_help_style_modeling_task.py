from datetime import datetime


class HumanHelpStyleModelingTask:
    """
    Modela estilos de ayuda humana y su efectividad.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        help_events = cognitive.get("learned_lessons", [])
        evaluations = cognitive.get("plan_result_evaluations", [])

        if not help_events or not evaluations:
            return None

        styles = cognitive.setdefault("human_help_styles", {})

        for lesson, eval_ in zip(help_events[-5:], evaluations[-5:]):
            style = lesson.get("style", "unknown")
            result = eval_.get("result")

            stats = styles.setdefault(
                style,
                {"successful": 0, "weak": 0, "failed": 0}
            )

            if result in stats:
                stats[result] += 1

        guardian["human_help_styles_updated_at"] = datetime.utcnow().isoformat()

        self.memory.log_event(
            event="human_help_styles_modeled",
            summary=f"Estilos de ayuda humana actualizados ({len(styles)})"
        )
        self.memory._persist()

        return styles