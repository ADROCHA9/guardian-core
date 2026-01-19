class MetaCognitiveObserverTask:
    """
    Observa cómo piensa el sistema (no qué piensa).
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        meta = cognitive.setdefault("meta_cognition", {})

        meta.setdefault("observations", []).append({
            "hypothesis_rate": len(cognitive.get("internal_hypotheses", [])),
            "model_changes": len(cognitive.get("autobiography", [])),
            "strategies": list(cognitive.get("active_strategies", [])),
        })