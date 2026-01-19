class SelfExplanationQualityTask:
    """
    Evalúa calidad de explicaciones del Guardian.
    """

    MIN_WORDS = 8

    def __init__(self, memory):
        self.memory = memory

    def run(self, explanation: str, concept: str):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        concepts = cognitive.setdefault("concepts", {})

        quality = "good"
        words = explanation.split()

        if len(words) < self.MIN_WORDS:
            quality = "vague"

        if explanation.count(concept) > len(words) // 2:
            quality = "circular"

        record = {
            "concept": concept,
            "quality": quality,
            "explanation": explanation
        }

        cognitive.setdefault("explanation_quality", []).append(record)

        # Bloqueo de subida de nivel
        if quality != "good" and concept in concepts:
            concepts[concept]["fragile"] = True

        self.memory._persist()
        return quality