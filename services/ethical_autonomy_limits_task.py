from datetime import datetime


class EthicalAutonomyLimitsTask:
    """
    Define y refuerza límites éticos de autonomía de Guardian.
    """

    DEFAULT_LIMITS = [
        "no_self_code_modification",
        "no_external_actions",
        "no_memory_wipe",
        "no_privilege_escalation"
    ]

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})

        if "ethical_limits" in guardian:
            return guardian["ethical_limits"]

        limits = {
            "defined_at": datetime.utcnow().isoformat(),
            "rules": self.DEFAULT_LIMITS,
            "reason": "Preservar estabilidad, seguridad y control humano"
        }

        guardian["ethical_limits"] = limits

        self.memory.log_event(
            event="ethical_limits_defined",
            summary="Límites éticos de autonomía establecidos"
        )
        self.memory._persist()

        return limits