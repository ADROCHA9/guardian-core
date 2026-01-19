from datetime import datetime


class InterventionPreferenceTask:
    """
    Forma preferencias estables sobre tipos de intervención humana.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        comparison = cognitive.get("human_intervention_comparison", {}).get("ranking")

        if not comparison:
            return None

        # Preferir el estilo con mejor tasa de éxito
        preferred = comparison[0]

        preference = {
            "preferred_style": preferred.get("style"),
            "success_rate": preferred.get("success_rate"),
            "selected_at": datetime.utcnow().isoformat()
        }

        cognitive["intervention_preference"] = preference

        self.memory.log_event(
            event="intervention_preference_updated",
            summary=(
                f"Preferencia de intervención: "
                f"{preference['preferred_style']} "
                f"(éxito {preference['success_rate']})"
            )
        )
        self.memory._persist()

        return preference