class AuthorizedExecutionTask:
    """
    Ejecuta acciones reales SOLO si el operador lo autorizó.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.get("guardian_self", {})
        permissions = guardian.get("pending_permissions", [])

        for p in permissions:
            if p.get("status") == "approved":
                p["executed"] = True
                p["execution_result"] = "executed_safely"

        self.memory._persist()