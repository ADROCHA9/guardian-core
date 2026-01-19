# security/voice/audio_capture.py
import sounddevice as sd
import numpy as np


def capture_voice(
    duration: float = 4.0,
    samplerate: int = 16000
) -> bytes:
    """
    Captura audio real desde el micrófono.
    Devuelve bytes PCM.
    """
    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="int16"
    )
    sd.wait()

    audio_bytes = recording.tobytes()
    return audio_bytes