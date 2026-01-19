from datetime import datetime


class SelfDesignLimitDetectionTask:
    """
    Detecta límites del propio diseño de Guardian.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        limits = []

        # Límite de memoria
        limits.append("La memoria no es infinita; requiere compresión constante.")

        # Límite de loop
        limits.append("El loop cognitivo prioriza estabilidad sobre velocidad.")

        # Límite de auto-modificación
        limits.append("La auto-modificación debe ser gradual y reversible.")

        detected = {
            "detected_at": datetime.utcnow().isoformat(),
            "limits": limits
        }

        self.memory._memory.setdefault("guardian_self", {})[
            "design_limits"
        ] = detected

        self.memory._persist()
        return detected