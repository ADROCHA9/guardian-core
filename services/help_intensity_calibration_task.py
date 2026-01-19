from datetime import datetime


class HelpIntensityCalibrationTask:
    """
    Ajusta cuánta ayuda humana pedir (low / medium / high).
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        trust = guardian.get("human_trust_level", 0.5)

        evaluations = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("plan_result_evaluations", [])
        )

        recent = evaluations[-3:]
        failures = len([e for e in recent if e.get("result") == "failed"])

        if failures >= 2 and trust > 0.6:
            level = "high"
        elif failures == 1:
            level = "medium"
        else:
            level = "low"

        guardian["help_intensity"] = {
            "level": level,
            "calibrated_at": datetime.utcnow().isoformat()
        }

        self.memory.log_event(
            event="help_intensity_calibrated",
            summary=f"Nivel de ayuda humana: {level}"
        )
        self.memory._persist()

        return level