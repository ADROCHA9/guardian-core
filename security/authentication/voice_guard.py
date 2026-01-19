# security/authentication/voice_guard.py
from security.authentication.voice_auth import extract_voice_signature


def register_voice_identity(memory, audio_bytes: bytes):
    """
    Registra la huella biométrica (solo una vez, en nacimiento).
    """
    identity = memory.get("identity", {})

    # 🔒 Si ya existe huella, no sobrescribir
    if "voice_hash" in identity:
        return

    identity["voice_hash"] = extract_voice_signature(audio_bytes)

    memory.log_event(
        event="voice_registered",
        summary="Huella de voz registrada"
    )

    memory._persist()