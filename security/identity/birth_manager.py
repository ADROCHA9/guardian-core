# security/identity/birth_manager.py
from datetime import datetime
from security.voice.voice_registry import register_voice


def perform_birth(memory, audio_bytes: bytes, password: str) -> None:
    """
    Ejecuta el nacimiento real del Guardian.
    """

    voice_hash = register_voice(audio_bytes)

    memory._memory["identity"] = {
        "operator": memory.get("conscious_state", {}).get("operator"),
        "voice_hash": voice_hash,
        "password_set": True,
        "born_at": datetime.utcnow().isoformat(),
        "status": "alive"
    }

    memory._memory.setdefault("guardian_self", {})
    memory._memory["guardian_self"].update({
        "status": "alive",
        "evolution_level": 1,
        "birth_confirmed": True
    })

    memory.log_event(
        event="guardian_born",
        summary="Nacimiento real del Guardian confirmado"
    )

    memory._persist()