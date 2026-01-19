from datetime import datetime


class DeepMemoryOptimizationTask:
    """
    Optimiza profundamente la memoria:
    - une ideas redundantes
    - elimina basura cognitiva
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        events = cognitive.get("events", [])

        # Convertir eventos repetidos en estadística
        summarized = list({e.get("event") for e in events})

        cognitive["events"] = summarized
        cognitive["memory_optimized_at"] = datetime.utcnow().isoformat()

        self.memory._persist()
        return summarized