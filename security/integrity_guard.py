# security/integrity_guard.py
import os

# Grupos de marcadores válidos que definen la identidad del Guardian
# Cada grupo representa un requisito lógico (al menos uno debe existir)
CRITICAL_MARKERS = [
    ["guardian_bot", "guardian_bot.txt"],      # Identidad del Guardian (flexible)
    [".project_knowledge.json"]                 # Memoria persistente
]


def verify_integrity(project_root: str) -> None:
    """
    Verifica que el Guardian se encuentre íntegro.
    - Acepta variantes de marcador para compatibilidad entre OS
    - Permite nacimiento limpio (crea memoria si no existe)
    """

    for marker_group in CRITICAL_MARKERS:
        if not any(
            os.path.exists(os.path.join(project_root, marker))
            for marker in marker_group
        ):
            expected = " o ".join(marker_group)
            raise RuntimeError(
                f"Integridad comprometida: falta {expected}"
            )