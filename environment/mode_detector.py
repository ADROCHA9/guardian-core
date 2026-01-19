# environment/mode_detector.py
from environment.os_probe import os_present

def detect_mode(boot_context: dict | None = None) -> dict:
    """
    boot_context puede ser inyectado por:
    - bootloader del Guardian
    - entorno embedded
    """

    if boot_context and boot_context.get("guardian_primary_boot"):
        if boot_context.get("embedded"):
            return {"mode": "FIRMWARE", "description": "Guardian en entorno bare-metal"}
        return {"mode": "SYSTEM", "description": "Guardian como sistema primario"}

    if os_present():
        return {"mode": "USER", "description": "Sistema operativo presente"}

    # Fallback explícito
    return {"mode": "UNKNOWN", "description": "Contexto no determinado"}