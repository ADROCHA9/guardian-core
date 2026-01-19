class ConceptDependencyResolverTask:
    """
    Detecta dependencias entre conceptos.
    """

    DEPENDENCIES = {
        "recursion": ["function"],
        "loop": ["iterable"],
        "list_comprehension": ["loop", "list"],
    }

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        concepts = cognitive.get("concepts", {})
        resolved = {}

        for concept, deps in self.DEPENDENCIES.items():
            missing = [d for d in deps if d not in concepts or concepts[d]["level"] < 2]
            if missing:
                resolved[concept] = {
                    "missing_dependencies": missing,
                    "reason": f"No conviene practicar {concept} sin {missing}"
                }

        cognitive["concept_dependencies"] = resolved
        self.memory._persist()
        return resolved