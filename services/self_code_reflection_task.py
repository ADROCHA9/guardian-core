import ast
import os

class SelfCodeReflectionTask:
    """
    Guardian se lee a sí mismo para aprender Python aplicado.
    """

    def __init__(self, memory):
        self.memory = memory
        self.root = memory.root_path

    def run(self):
        functions = []

        for root, _, files in os.walk(self.root):
            for f in files:
                if not f.endswith(".py"):
                    continue
                path = os.path.join(root, f)

                try:
                    tree = ast.parse(open(path, "r", encoding="utf-8").read())
                except Exception:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append(node.name)

        self.memory.log_event(
            event="self_reflection",
            summary=f"Funciones propias detectadas: {len(functions)}"
        )
        self.memory._persist()
        return functions