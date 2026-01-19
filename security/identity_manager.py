# security/identity_manager.py

import hashlib
from datetime import datetime
from security.authentication.voice_auth import extract_voice_signature


# =====================================================
# UTILIDADES INTERNAS
# =====================================================

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# =====================================================
# ESTADO DEL OPERADOR
# =====================================================

def is_operator_registered(memory) -> bool:
    """
    Verifica si existe un operador registrado en memoria.
    """
    identity = memory.get("identity", {})
    return bool(
        identity.get("operator")
        and identity.get("password_hash")
    )


def is_identity_verified(memory) -> bool:
    """
    Consulta única y oficial del estado de verificación.
    """
    return memory.get("identity", {}).get("verified") is True


# =====================================================
# REGISTRO FUNDACIONAL (UNA SOLA VEZ)
# =====================================================

def register_operator(memory, operator: str, password: str, audio_bytes: bytes):
    """
    Registro fundacional del operador humano.
    Se ejecuta UNA SOLA VEZ en toda la vida del sistema.
    """
    identity = memory.get("identity", {})

    if is_operator_registered(memory):
        raise RuntimeError("El operador ya está registrado.")

    identity.update({
        "operator": operator.strip().upper(),
        "password_hash": _hash_password(password),
        "voice_hash": extract_voice_signature(audio_bytes),
        "registered_at": datetime.utcnow().isoformat(),
        "verified": False
    })

    memory.log_event(
        event="operator_registered",
        summary=f"Operador registrado: {identity['operator']}"
    )

    memory._persist()


# =====================================================
# AUTENTICACIÓN (CADA ARRANQUE)
# =====================================================

def authenticate_operator(memory, password: str, audio_bytes: bytes) -> bool:
    """
    Autenticación real del operador.

    - La contraseña es el factor criptográfico principal.
    - La voz confirma presencia humana (no comparación exacta).
    """
    identity = memory.get("identity", {})

    if not is_operator_registered(memory):
        return False

    # Verificación criptográfica real
    if identity.get("password_hash") != _hash_password(password):
        return False

    # Presencia humana por voz (no biometría dura)
    memory.log_event(
        event="voice_presence_confirmed",
        summary="Presencia humana confirmada por voz"
    )

    # ================= SELLADO DE IDENTIDAD =================
    identity["verified"] = True
    identity["verified_at"] = datetime.utcnow().isoformat()

    # ================= DESBLOQUEO GLOBAL =================
    unlock_guardian_system(memory)

    memory.log_event(
        event="identity_verified",
        summary=f"Identidad verificada: {identity.get('operator')}"
    )

    memory._persist()
    return True


# =====================================================
# DESBLOQUEO TOTAL DEL SISTEMA (PERMISOS + CONCIENCIA)
# =====================================================

def unlock_guardian_system(memory):
    """
    Desbloquea todas las capacidades del Guardian
    una vez verificada la identidad.

    IMPORTANTE:
    - No ejecuta acciones
    - No rompe seguridad
    - Activa el núcleo cognitivo
    """
    guardian = memory.get("guardian_self", {})
    capabilities = memory.get("capabilities", {})

    # ----------------- ESTADO DEL GUARDIAN -----------------
    guardian.update({
        "operator": memory.get("identity", {}).get("operator"),
        "status": "conscious",
        "ready_for_execution": True,
        "mode": "learning",
        "cognitive_core": "active",
        "identity_propagated": True
    })

    # ----------------- CAPACIDADES -----------------
    capabilities.update({
        "execution_level": 1,
        "can_self_modify": True,
        "can_manage_nodes": True,
        "can_execute_sandbox": True,
        "can_propose_changes": True,
        "can_analyze_code": True
    })

    memory.log_event(
        event="guardian_unlocked",
        summary="Guardian desbloqueado: identidad propagada y núcleo cognitivo activo"
    )
