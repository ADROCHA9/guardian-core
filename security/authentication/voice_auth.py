# security/authentication/voice_auth.py
import hashlib
import numpy as np


def extract_voice_signature(audio_bytes: bytes) -> str:
    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)

    if audio.size == 0:
        raise ValueError("Audio vacío")

    audio /= (np.max(np.abs(audio)) + 1e-9)

    rms = float(np.sqrt(np.mean(audio * audio)))
    energy = float(np.sum(audio * audio))

    raw = f"{rms:.6f}:{energy:.6f}"
    return hashlib.sha256(raw.encode()).hexdigest()


def verify_voice(sig_new: str, sig_stored: str) -> bool:
    return sig_new == sig_stored