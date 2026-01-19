import ast
from datetime import datetime


class IntentionalPythonLearningTask:
    """
    Aprendizaje intencional de Python sin IA externa.
    """

    def __init__(self, memory, topic: str):
        self.memory = memory
        self.topic = topic.lower()

    def run(self):
        learned = []

        if "funcion" in self.topic:
            code = """
def ejemplo(a, b):
    return a + b
"""
            tree = ast.parse(code)

            learned.append({
                "concept": "function",
                "example": code.strip(),
                "ast_nodes": [type(n).__name__ for n in ast.walk(tree)]
            })

        snapshot = self.memory._memory
        cognitive = snapshot.setdefault("cognitive_memory", {})
        python_knowledge = cognitive.setdefault("python_knowledge", {})

        for item in learned:
            concept = item.get("concept", "general")
            bucket = python_knowledge.setdefault(concept, [])
            bucket.append(item)

        guardian = snapshot.setdefault("guardian_self", {})
        guardian["learning_state"] = "intentional"

        self.memory.log_event(
            event="python_intentional_learning",
            summary=f"Aprendizaje intencional: {self.topic}"
        )

        self.memory._persist()
        return learned