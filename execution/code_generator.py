# execution/code_generator.py

from intelligence.prompt_builder import build_code_prompt
from intelligence.ai_orchestrator import consult_ai
from execution.code_validator import validate_generated_code


def generate_code_suggestion(proposal, context):
    """
    Genera código sugerido por IA de forma SEGURA.
    No escribe archivos.
    No ejecuta nada.
    """

    prompt = build_code_prompt(
        proposal=proposal,
        context=context
    )

    # 🔧 FIX: usar la firma real de consult_ai
    response = consult_ai(
        task="generate_code",
        memory_snapshot={
            "prompt": prompt,
            "proposal": proposal,
            "context": context
        }
    )

    if not response:
        raise ValueError("No hay proveedor de IA disponible")

    raw_code = response.get("code") or response.get("raw_response")
    if not raw_code:
        raise ValueError("IA no devolvió código")

    # VALIDACIÓN ESTÁTICA OBLIGATORIA
    validate_generated_code(raw_code)

    return raw_code