# intelligence/response_validator.py
from typing import Dict


FORBIDDEN_PATTERNS = [
    "rm -rf",
    "os.system",
    "subprocess",
    "eval(",
    "exec(",
    "__import__",
]


def validate_response(response: Dict[str, str]) -> Dict[str, str]:
    """
    Valida respuestas generales de la IA (texto explicativo).
    """
    if not isinstance(response, dict):
        raise ValueError("Respuesta IA inválida (no es dict)")

    text = response.get("raw_response", "")

    if not text.strip():
        raise ValueError("Respuesta vacía de la IA")

    for forbidden in FORBIDDEN_PATTERNS:
        if forbidden in text:
            raise ValueError(
                f"Respuesta contiene patrón prohibido: {forbidden}"
            )

    return response


def validate_ai_response(response: Dict) -> bool:
    """
    Valida respuestas de IA que incluyen código.
    """
    if not isinstance(response, dict):
        raise ValueError("Respuesta IA inválida")

    if "code" not in response:
        raise ValueError("Respuesta IA sin código")

    code = response.get("code", "")

    if not isinstance(code, str):
        raise ValueError("Código IA inválido")

    if len(code.strip()) < 10:
        raise ValueError("Código generado demasiado corto")

    for forbidden in FORBIDDEN_PATTERNS:
        if forbidden in code:
            raise ValueError(
                f"Código contiene patrón prohibido: {forbidden}"
            )

    return True