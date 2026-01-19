from typing import Dict, Optional

from intelligence.ai_registry import detect_ai_providers
from intelligence.ollama_client import OllamaClient
from intelligence.ai_consultant import AIConsultant
from intelligence.prompt_builder import build_prompt
from security.firewall import scan_text


def consult_ai(
    task: str,
    memory_snapshot: Dict,
    preferred_model: Optional[str] = None
) -> Optional[Dict[str, str]]:
    """
    Orquesta una consulta segura a una IA consultora (Ollama).
    Devuelve la respuesta validada o None si no hay IA disponible.
    """

    providers = detect_ai_providers()

    if not providers:
        return None

    ollama_info = providers[0]
    models = ollama_info.get("models", [])

    if not models:
        return None

    model = preferred_model if preferred_model in models else models[0]

    client = OllamaClient(model)
    consultant = AIConsultant(client, "ollama")

    prompt = build_prompt(
        task=task,
        memory_snapshot=memory_snapshot
    )

    response = consultant.consult(prompt)

    # 🔐 Firewall de seguridad
    scan_text(response["raw_response"])

    return response