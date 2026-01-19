# services/module_integration_task.py

class ModuleIntegrationTask:
    """
    Define un plan de integración progresiva de módulos.
    NO ejecuta cambios.
    """

    PRIORITY_ORDER = [
        "orchestration",
        "cognitive_core",
        "memory",
        "execution_control",
        "interface"
    ]

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        recognition = self._get_last_self_recognition()
        if not recognition:
            return None

        summary = recognition.get("summary", {})
        plan = []

        for role in self.PRIORITY_ORDER:
            if role in summary:
                plan.append({
                    "module_type": role,
                    "count": summary[role],
                    "reason": self._reason_for(role)
                })

        return {
            "type": "integration_plan",
            "steps": plan,
            "principle": "stability_before_features"
        }

    def _get_last_self_recognition(self):
        decisions = self.memory._memory.get("cognitive_memory", {}).get("decisions", [])
        for d in reversed(decisions):
            if d.get("decision") == "self_recognition_completed":
                return d
        return None

    def _reason_for(self, role: str) -> str:
        reasons = {
            "orchestration": "coordinar pensamiento y reducir carga",
            "cognitive_core": "centralizar decisiones",
            "memory": "estabilidad y consistencia",
            "execution_control": "seguridad antes de acción",
            "interface": "visualización, no control"
        }
        return reasons.get(role, "orden lógico")