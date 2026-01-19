# security/voice/voice_registry.py
import os
import hashlib


VOICE_DIR = "security/voice/data"


def register_voice(audio_bytes: bytes) -> str:
    """
    Registra una huella biométrica simple de voz.
    """
    os.makedirs(VOICE_DIR, exist_ok=True)

    voice_hash = hashlib.sha256(audio_bytes).hexdigest()
    path = os.path.join(VOICE_DIR, f"{voice_hash}.voice")

    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(audio_bytes)

    return voice_hash


def voice_exists(voice_hash: str) -> bool:
    return os.path.exists(
        os.path.join(VOICE_DIR, f"{voice_hash}.voice")
    )