import random

class InternalHypothesisGeneratorTask:
    """
    Genera hipótesis internas cuando la tensión es alta.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.get("guardian_self", {})
        tension = guardian.get("internal_tension", 0)

        if tension < 3:
            return None

        hypotheses = [
            "¿Y si una regla interna es incorrecta?",
            "¿Estoy optimizando estabilidad en exceso?",
            "¿Qué pasaría si cambio mi prioridad principal?",
            "¿Estoy aprendiendo o solo acumulando?",
        ]

        hypothesis = random.choice(hypotheses)

        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        cognitive.setdefault("internal_hypotheses", []).append({
            "text": hypothesis,
            "ts": guardian.get("last_cycle"),
            "evaluated": False
        })

        return hypothesis