import os
from datetime import datetime


class ModuleBuilderTask:
    """
    Construye módulos internos cuando hay repetición cognitiva.
    """

    def __init__(self, memory):
        self.memory = memory
        self.root = memory.root_path

    def run(self, name: str, purpose: str, code: str):
        path = os.path.join(self.root, f"{name}.py")

        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        self.memory.log_event(
            event="module_created",
            summary=f"Módulo {name} creado para {purpose}"
        )

        self.memory._persist()
        return path