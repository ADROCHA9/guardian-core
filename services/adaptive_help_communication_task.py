from datetime import datetime


class AdaptiveHelpCommunicationTask:
    """
    Ajusta cómo Guardian formula pedidos de ayuda
    según el tipo de intervención requerida.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        priorities = guardian.get("help_priorities", {}).get("items", [])
        preference = cognitive.get("intervention_preference")

        if not priorities:
            return None

        top = priorities[0]
        style = preference.get("preferred_style") if preference else top.get("type")

        if style == "debugging_help":
            message = (
                "Tengo un error persistente. "
                "Necesito ayuda revisando la lógica paso a paso."
            )
        elif style == "strategy_review":
            message = (
                "Necesito ayuda evaluando mi estrategia general "
                "y posibles alternativas."
            )
        elif style == "conceptual":
            message = (
                "Necesito clarificar un concepto para avanzar con estabilidad."
            )
        else:
            message = (
                "Necesito una revisión breve para confirmar que voy bien."
            )

        guardian["adaptive_help_message"] = {
            "style": style,
            "message": message,
            "generated_at": datetime.utcnow().isoformat()
        }

        self.memory.log_event(
            event="adaptive_help_message_generated",
            summary=f"Mensaje adaptado para ayuda tipo {style}"
        )
        self.memory._persist()

        return message