# execution/diff_engine.py
import difflib
from typing import List


def generate_diff(
    original: str,
    modified: str,
    filename: str = "file.py"
) -> List[str]:
    """
    Genera un diff unificado entre dos versiones de código.

    No escribe archivos.
    No ejecuta nada.
    Solo devuelve texto del diff.
    """

    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)

    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"{filename} (original)",
        tofile=f"{filename} (propuesto)",
        lineterm=""
    )

    return list(diff)