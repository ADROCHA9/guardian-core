from datetime import datetime


def reset_guardian_memory(memory):
    """
    Resetea completamente la memoria cognitiva de Guardian,
    conservando identidad y entorno.
    """

    old_identity = memory.get("identity", {})
    environment = memory.get("environment", {})
    capabilities = memory.get("capabilities", {})

    memory._memory.clear()

    # ================= IDENTIDAD =================
    memory._memory["identity"] = {
        **old_identity,
        "status": "alive"
    }

    # ================= GUARDIAN SELF =================
    memory._memory["guardian_self"] = {
        "identity": "Guardian",
        "operator": old_identity.get("operator") or "human",
        "authority_model": "human_in_the_loop",
        "status": "idle",
        "evolution_level": 1,
        "birth_confirmed": True,
        "ready_for_execution": False,
        "last_cycle": None,
        "initialized_at": datetime.utcnow().isoformat()
    }

    # ================= CONCIENCIA =================
    memory._memory["conscious_state"] = {
        "mode": "active"
    }

    # ================= CAPACIDADES =================
    memory._memory["capabilities"] = capabilities or {
        "can_execute_sandbox": True,
        "can_propose_changes": True,
        "can_analyze_code": True
    }

    # ================= ENTORNO =================
    memory._memory["environment"] = environment

    # ================= ESTADO COGNITIVO LIMPIO =================
    memory._memory["open_questions"] = []
    memory._memory["proposed_connections"] = []
    memory._memory["decision_log"] = []
    memory._memory["backups"] = []
    memory._memory["services"] = {
        "continuous_work": "active"
    }

    # ================= LOG =================
    memory.log_event(
        event="guardian_memory_reset",
        summary="Memoria reseteada e inicializada con arquitectura final."
    )

    memory._persist()