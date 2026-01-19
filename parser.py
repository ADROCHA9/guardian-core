# parser.py
import ast
import hashlib
from typing import Dict, Any, List


def parse_python_file(
    absolute_path: str,
    relative_path: str
) -> Dict[str, Any]:

    with open(absolute_path, "r", encoding="utf-8") as f:
        source = f.read()

    file_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()

    imports: List[str] = []
    classes: List[str] = []
    functions: List[str] = []

    syntax_error = None

    try:
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([n.name for n in node.names])

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)

    except SyntaxError as e:
        syntax_error = f"{e.msg} (línea {e.lineno})"

    role = infer_role(relative_path, classes, functions)

    return {
        "type": "module",
        "language": "python",
        "role": role,
        "status": "activo" if not syntax_error else "sintaxis_inválida",
        "_source": source,
        "_hash": file_hash,
        "confidence": 0.7 if not syntax_error else 0.2,

        "structure": {
            "imports": imports,
            "classes": classes,
            "functions": functions
        },

        "intent": {
            "what_it_does": role,
            "why_it_exists": "pendiente de confirmación"
        },

        "relations": {
            "depends_on": imports,
            "used_by": [],
            "missing_links": []
        },

        "issues": (
            [{
                "type": "syntax_error",
                "description": syntax_error
            }] if syntax_error else []
        ),

        "notes": []
    }


# -------------------------
# HEURÍSTICA DE ROL
# -------------------------
def infer_role(
    path: str,
    classes: List[str],
    functions: List[str]
) -> str:

    name = path.lower()

    if "core" in name or "neuro" in name:
        return "núcleo orquestador"

    if "sandbox" in name:
        return "entorno de prueba aislado"

    if "security" in name or "ethic" in name:
        return "control y validación"

    if classes and not functions:
        return "definición estructural"

    if functions and not classes:
        return "lógica funcional"

    return "módulo auxiliar"