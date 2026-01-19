import random

class MetaHypothesisGeneratorTask:
    """
    Genera hipótesis sobre el propio proceso cognitivo.
    """

    META_HYPOTHESES = [
        "¿Estoy penalizando demasiado el error?",
        "¿Evito cambiar reglas centrales por inercia?",
        "¿Mi creatividad es demasiado conservadora?",
        "¿Estoy optimizando estabilidad en exceso?",
        "¿Aprendo mejor explorando o refinando?"
    ]

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        meta = cognitive.setdefault("meta_cognition", {})

        hypothesis = random.choice(self.META_HYPOTHESES)

        meta.setdefault("meta_hypotheses", []).append({
            "text": hypothesis,
            "evaluated": False
        })

        return hypothesis