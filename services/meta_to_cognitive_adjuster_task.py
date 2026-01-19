class MetaToCognitiveAdjusterTask:
    """
    Traduce conclusiones meta-cognitivas en ajustes suaves.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})
        meta = cognitive.get("meta_cognition", {})

        for h in meta.get("meta_hypotheses", []):
            if not h.get("valid"):
                continue

            text = h["text"]

            if "demasiado conservadora" in text:
                guardian["creativity_bias"] = guardian.get("creativity_bias", 1.0) * 1.1

            if "penalizando demasiado el error" in text:
                guardian["error_tolerance"] = guardian.get("error_tolerance", 1.0) * 1.1