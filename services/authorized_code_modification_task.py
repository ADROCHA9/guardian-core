class AuthorizedCodeModificationTask:
    """
    Ejecuta propuestas solo si el operador autorizó.
    """

    def __init__(self, memory, executor):
        self.memory = memory
        self.executor = executor

    def run(self):
        guardian = self.memory._memory.get("guardian_self", {})
        permissions = guardian.get("pending_permissions", [])
        proposals = self.memory._memory.get("cognitive_memory", {}).get("module_refactor_proposals", {}).get("proposals", [])

        for p in permissions:
            if p["status"] == "approved" and p["action"] == "code_refactor":
                def apply():
                    # ⚠️ Aquí solo se integrará/eliminará código SIMPLE
                    # (los detalles se refinarán más adelante)
                    pass

                result = self.executor.execute(apply)
                p["execution_result"] = result

        self.memory._persist()