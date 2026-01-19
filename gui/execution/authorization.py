# execution/authorization.py
from security.identity_manager import ensure_identity


def authorize_execution(memory, password: str) -> bool:
    """
    Verifica que el operador tiene autoridad para ejecutar cambios reales.
    """
    identity = memory.get("identity")
    if not identity:
        return False

    # Reutilizamos ensure_identity solo para password
    return ensure_identity(
        memory=memory,
        audio_bytes=b"",   # no pedimos voz de nuevo
        password=password
    )