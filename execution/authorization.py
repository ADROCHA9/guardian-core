# execution/authorization.py
from datetime import datetime


def authorize_execution(
    memory,
    reason: str = ""
) -> bool:
    """
    Autoriza la ejecución de cambios reales.
    Debe llamarse SOLO tras confirmación humana.
    """

    identity = memory.get("identity") or {}

    # =====================================================
    # Verificación de identidad
    # =====================================================
    if not identity:
        raise RuntimeError("No existe identidad registrada")

    if not identity.get("born_at"):
        raise RuntimeError("Guardian no ha nacido")

    # =====================================================
    # Registro de autorización
    # =====================================================
    memory._memory.setdefault("execution_authorizations", [])
    memory._memory["execution_authorizations"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "reason": reason or "manual approval",
        "operator": identity.get("operator")
    })

    memory.log_event(
        event="execution_authorized",
        summary=reason or "Ejecución autorizada por el operador"
    )

    memory._persist()
    return True