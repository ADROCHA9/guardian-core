from intelligence.ai_orchestrator import consult_ai

class GuidedLearningTask:
    """
    Aprende conceptos con IA externa SIN ejecutar nada.
    """

    def __init__(self, memory, topic: str):
        self.memory = memory
        self.topic = topic

    def run(self) -> dict:
        response = consult_ai(
            task=f"Explicar buenas prácticas sobre: {self.topic}",
            memory_snapshot=self.memory._memory
        )

        self.memory.setdefault("cognitive_memory", {}).setdefault(
            "learned_topics", []
        ).append({
            "topic": self.topic,
            "source": "external_ai",
            "summary": response.get("raw_response", "")
        })

        self.memory._persist()

        return {
            "topic": self.topic,
            "learned": True
        }