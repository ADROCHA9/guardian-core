# execution/code_validator.py
import ast

FORBIDDEN_IMPORTS = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "ctypes"
}

FORBIDDEN_CALLS = {
    "eval",
    "exec",
    "compile",
    "open",
    "__import__"
}


def validate_generated_code(code: str):
    """
    Valida código generado por IA.
    Lanza excepción si no es seguro.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Código inválido: {e}")

    for node in ast.walk(tree):
        # imports prohibidos
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name.split(".")[0] in FORBIDDEN_IMPORTS:
                    raise ValueError(f"Import prohibido: {name.name}")

        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                raise ValueError(f"Import prohibido: {node.module}")

        # llamadas prohibidas
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in FORBIDDEN_CALLS:
                    raise ValueError(f"Llamada prohibida: {node.func.id}")

    return True