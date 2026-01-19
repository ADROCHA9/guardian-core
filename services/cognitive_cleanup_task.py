import time


class CognitiveCleanupTask:
    """
    Limpieza cognitiva inteligente.
    """

    MAX_UNUSED_DAYS = 30

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        concepts = cognitive.get("concepts", {})
        now = time.time()

        to_delete = []

        for name, c in concepts.items():
            last = c.get("last_update") or now
            if (
                c["uses"] <= 1
                and not c["dominated"]
                and (now - last) > self.MAX_UNUSED_DAYS * 86400
            ):
                to_delete.append(name)

        for name in to_delete:
            del concepts[name]

        # Compactar eventos repetidos
        cognitive["raw_ideas"] = cognitive.get("raw_ideas", [])[-10:]

        self.memory._persist()