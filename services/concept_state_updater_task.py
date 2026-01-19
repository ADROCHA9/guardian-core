import time


class ConceptStateUpdaterTask:
    """
    Mantiene Concept Knowledge Units (CKU).
    """

    def __init__(self, memory):
        self.memory = memory

    def _concepts(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        return cognitive.setdefault("concepts", {})

    def update_from_test(self, concepts: list, test_result: dict):
        concepts_mem = self._concepts()

        for name in concepts:
            c = concepts_mem.setdefault(name, {
                "level": 0,
                "uses": 0,
                "passes": 0,
                "fails": 0,
                "fragile": False,
                "dominated": False,
                "last_update": None
            })

            c["uses"] += 1
            c["last_update"] = time.time()

            if test_result["passed"]:
                c["passes"] += 1
                if c["passes"] >= 2:
                    c["level"] = min(c["level"] + 1, 5)
            else:
                c["fails"] += 1
                c["fragile"] = True
                if c["level"] > 0:
                    c["level"] -= 1

            # Dominio real
            if c["level"] >= 4 and c["fails"] == 0:
                c["dominated"] = True
                c["fragile"] = False

        self.memory._persist()