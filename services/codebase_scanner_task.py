import os
from datetime import datetime


class CodebaseScannerTask:
    """
    Escanea la carpeta raíz y analiza módulos Python.
    """

    def __init__(self, root_path, memory):
        self.root = root_path
        self.memory = memory

    def run(self):
        modules = []

        for root, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py"):
                    path = os.path.join(root, f)
                    modules.append({
                        "path": path,
                        "name": f,
                        "size": os.path.getsize(path)
                    })

        self.memory._memory.setdefault("cognitive_memory", {})[
            "codebase_modules"
        ] = {
            "scanned_at": datetime.utcnow().isoformat(),
            "modules": modules
        }

        self.memory._persist()
        return modules