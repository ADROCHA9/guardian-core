class CognitiveCapabilityLimiterTask:
    """
    Limita capacidades según evidencia real de madurez cognitiva.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})

        evo = guardian.get("unlocked_stages", [])
        autobiography = cognitive.get("autobiography", [])
        meta = cognitive.get("meta_cognition", {})

        level = 0

        if "reflection" in evo and len(autobiography) >= 10:
            level = 1

        if level == 1 and len(meta.get("meta_hypotheses", [])) >= 5:
            level = 2

        if level == 2:
            valid = [h for h in meta.get("meta_hypotheses", []) if h.get("valid")]
            if len(valid) >= 3:
                level = 3

        guardian["cognitive_level"] = level
        return level