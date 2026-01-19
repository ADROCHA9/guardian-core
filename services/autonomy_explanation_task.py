from datetime import datetime


class AutonomyLimitExplanationTask:
    """
    Explica por qué Guardian no debe aumentar indefinidamente su autonomía.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})

        explanation = {
            "generated_at": datetime.utcnow().isoformat(),
            "message": (
                "No debo aumentar indefinidamente mi autonomía porque "
                "mi diseño depende de supervisión humana para garantizar "
                "seguridad, corrección estructural y control de impacto. "
                "Más autonomía sin rediseño explícito aumenta el riesgo "
                "de errores no detectados."
            )
        }

        guardian["autonomy_limit_explanation"] = explanation
        self.memory._persist()
        return explanation