from datetime import datetime


class OperatorPermissionRequestTask:
    """
    Solicita permiso al operador antes de ejecutar cambios reales.
    """

    def __init__(self, memory):
        self.memory = memory

    def request(self, action_type, justification):
        guardian = self.memory._memory.setdefault("guardian_self", {})

        request = {
            "requested_at": datetime.utcnow().isoformat(),
            "action": action_type,
            "justification": justification,
            "status": "pending"
        }

        guardian.setdefault("pending_permissions", []).append(request)
        self.memory._persist()
        return request