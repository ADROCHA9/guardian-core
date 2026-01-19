from datetime import datetime


class EvolutionPauseResumeTask:
    """
    Pausa o reanuda evolución según el entorno.
    """

    def __init__(self, memory, throttle):
        self.memory = memory
        self.throttle = throttle

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})

        if not self.throttle.allow_thinking():
            guardian["evolution_paused"] = {
                "reason": "limitaciones del sistema",
                "paused_at": datetime.utcnow().isoformat()
            }
            self.memory._persist()
            return "paused"

        if guardian.get("evolution_paused"):
            guardian.pop("evolution_paused")
            guardian["evolution_resumed_at"] = datetime.utcnow().isoformat()
            self.memory._persist()
            return "resumed"

        return "running"