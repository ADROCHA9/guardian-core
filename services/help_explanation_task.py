from datetime import datetime


class HelpExplanationTask:
    """
    Explica claramente qué tipo de ayuda humana se necesita.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        priorities = guardian.get("help_priorities", {}).get("items", [])

        if not priorities:
            return None

        top = priorities[0]

        explanation = {
            "generated_at": datetime.utcnow().isoformat(),
            "message": (
                f"Necesito ayuda de tipo '{top['type']}' porque "
                f"{top['reason']}. "
                "Esto me permitiría avanzar de forma más eficiente."
            )
        }

        guardian["human_help_explanation"] = explanation

        self.memory.log_event(
            event="help_explained",
            summary=explanation["message"]
        )
        self.memory._persist()

        return explanation