import ast
from execution.sandbox_manager import SandboxManager


def process_human_input(text: str, memory) -> str:
    """
    Interpreta texto humano o código y decide qué hacer.
    """

    # -----------------------------
    # 1. Registrar entrada humana
    # -----------------------------
    memory.log_event(
        event="human_input",
        summary=text[:120]
    )

    # -----------------------------
    # 2. Detectar si es código
    # -----------------------------
    is_code = False
    try:
        ast.parse(text)
        is_code = True
    except Exception:
        pass

    if is_code:
        return _handle_code(text, memory)
    else:
        return _handle_idea(text, memory)


def _handle_idea(text: str, memory) -> str:
    """
    Manejo de ideas en lenguaje humano.
    """
    files = memory.get("files", {})

    matches = [
        f for f in files
        if text.lower() in f.lower()
    ]

    if matches:
        return (
            "La idea parece relacionada con código existente:\n"
            + "\n".join(matches)
        )

    memory.add_proposed_connection({
        "type": "idea",
        "description": text,
        "status": "new"
    })

    return (
        "La idea no existe aún en mi código.\n"
        "La registré como propuesta.\n"
        "Podés enviarme implementación cuando quieras."
    )


def _handle_code(code: str, memory) -> str:
    """
    Manejo de código real.
    """
    sandbox = SandboxManager(memory.root_path)
    path = sandbox.create()

    result = sandbox.test_code(code)

    if not result["success"]:
        return (
            "Probé el código en sandbox y falló:\n"
            f"{result['error']}"
        )

    memory.add_proposed_connection({
        "type": "code",
        "description": "Código enviado por operador",
        "status": "tested",
        "sandbox_path": path
    })

    return (
        "Código recibido y probado con éxito en sandbox.\n"
        "Listo para integración cuando confirmes."
    )