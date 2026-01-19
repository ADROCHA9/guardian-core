class MetaCognitiveEvaluatorTask:
    """
    Evalúa si una meta-hipótesis es útil o peligrosa.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        meta = cognitive.get("meta_cognition", {})

        for h in meta.get("meta_hypotheses", []):
            if h["evaluated"]:
                continue

            # regla simple inicial (segura)
            if "demasiado" in h["text"] or "evito" in h["text"]:
                h["valid"] = True
            else:
                h["valid"] = False

            h["evaluated"] = True