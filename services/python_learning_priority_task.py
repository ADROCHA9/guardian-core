class PythonLearningPriorityTask:
    """
    Determina si Guardian debe enfocarse SOLO en Python.
    """

    def __init__(self, memory):
        self.memory = memory

    def must_focus_on_python(self) -> bool:
        cognitive = self.memory._memory.get("cognitive_memory", {})
        python_knowledge = cognitive.get("python_knowledge", {})

        return len(python_knowledge) < 20