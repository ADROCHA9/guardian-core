# services/execution_transition.py

def can_execute_proposal(proposal: dict, memory) -> bool:
    """
    Verifica si una propuesta puede pasar a ejecución real.
    """
    guardian = memory.get("guardian_self", {})
    identity = memory.get("identity", {})

    return all([
        proposal.get("status") == "approved",
        identity.get("verified") is True,
        guardian.get("ready_for_execution") is True,
        guardian.get("identity_propagated") is True,
    ])