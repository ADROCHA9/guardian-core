from datetime import datetime


class HumanHelpLearningTask:
    """
    Extrae aprendizaje explícito de la ayuda humana recibida.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        help_request = guardian.get("human_help_requested")
        if not help_request or help_request.get("status") != "resolved":
            return None

        resolution = help_request.get("resolution")
        if not resolution:
            return None

        lesson = {
            "learned_at": datetime.utcnow().isoformat(),
            "lesson": resolution.get("summary"),
            "source": "human_help"
        }

        cognitive.setdefault("learned_lessons", []).append(lesson)

        # Aumentar confianza si ayudó
        guardian["human_trust_level"] = min(
            1.0,
            guardian.get("human_trust_level", 0.5) + 0.05
        )

        self.memory.log_event(
            event="human_help_learned",
            summary=f"Lección aprendida de ayuda humana: {lesson['lesson']}"
        )
        self.memory._persist()

        return lesson