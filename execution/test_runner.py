import os
from typing import Dict, List


class CodeGenerator:
    """
    Genera cambios de código dentro de una sandbox.
    No toca el proyecto real.
    """

    def __init__(self, sandbox_path: str):
        self.sandbox_path = sandbox_path
        self.changes: List[Dict] = []

    # --------------------------------------------------
    # UTILIDADES
    # --------------------------------------------------
    def _full_path(self, relative_path: str) -> str:
        return os.path.join(self.sandbox_path, relative_path)

    def _ensure_dir(self, file_path: str) -> None:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # --------------------------------------------------
    # OPERACIONES BÁSICAS
    # --------------------------------------------------
    def create_file(self, relative_path: str, content: str) -> None:
        path = self._full_path(relative_path)
        self._ensure_dir(path)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        self.changes.append({
            "action": "create_file",
            "file": relative_path
        })

    def modify_file(self, relative_path: str, new_content: str) -> None:
        path = self._full_path(relative_path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe {relative_path} en sandbox")

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        self.changes.append({
            "action": "modify_file",
            "file": relative_path
        })

    def append_to_file(self, relative_path: str, extra_content: str) -> None:
        path = self._full_path(relative_path)

        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe {relative_path} en sandbox")

        with open(path, "a", encoding="utf-8") as f:
            f.write("\n" + extra_content)

        self.changes.append({
            "action": "append_file",
            "file": relative_path
        })

    # --------------------------------------------------
    # PLANTILLAS ÚTILES (ejemplos reales)
    # --------------------------------------------------
    def generate_module(
        self,
        relative_path: str,
        description: str,
        dependencies: List[str] = None
    ) -> None:
        deps = dependencies or []

        content = f'''"""
{description}
"""

{"".join(f"import {d}\n" for d in deps)}

def main():
    """
    Punto de entrada del módulo.
    """
    pass


if __name__ == "__main__":
    main()
'''
        self.create_file(relative_path, content)

    # --------------------------------------------------
    # RESULTADO
    # --------------------------------------------------
    def get_changes(self) -> List[Dict]:
        return self.changes