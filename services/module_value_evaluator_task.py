class ModuleValueEvaluatorTask:
    """
    Evalúa el valor real de módulos creados.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self, module_name: str, before_errors: int, after_errors: int):
        value = before_errors - after_errors

        record = {
            "module": module_name,
            "value": value,
            "decision": "keep" if value > 0 else "discard"
        }

        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        cognitive.setdefault("module_evaluations", []).append(record)

        self.memory._persist()
        return record