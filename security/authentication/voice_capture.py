# security/authentication/voice_capture.py
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    sd = None


def record_voice(duration=4, samplerate=16000) -> bytes:
    """
    Graba audio real desde el micrófono.
    Devuelve bytes crudos normalizados.
    """
    if sd is None:
        raise RuntimeError("sounddevice no está instalado")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )
    sd.wait()

    # Normalizar y convertir a bytes
    audio = np.squeeze(recording)
    audio = audio / (np.max(np.abs(audio)) + 1e-6)

    return audio.tobytes()