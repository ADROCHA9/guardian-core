# execution/ai_consultation_step.py
from typing import Optional, Dict

from intelligence.ai_orchestrator import consult_ai


def run_ai_consultation(
    task: str,
    memory_snapshot: Dict
) -> Optional[str]:
    """
    Ejecuta una consulta consciente a una IA consultora.
    Devuelve texto o None si no hay IA disponible.
    """

    response = consult_ai(
        task=task,
        memory_snapshot=memory_snapshot
    )

    if response:
        return response["raw_response"]

    return None