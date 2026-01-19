from typing import Dict, List
from datetime import datetime

class EvolutionaryPlanningTask:
    """
    Decide QUÉ mejorar primero usando métricas reales.
    No ejecuta nada.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self) -> Dict:
        metrics = self.memory.get("metrics", {})
        guardian = self.memory.get("guardian_self", {})
        history = self.memory.get("evolution_decisions", [])

        priorities: List[Dict] = []

        # 🔍 Ejemplo de criterio real
        if metrics:
            if metrics["project"]["inconsistencies"] > 0:
                priorities.append({
                    "target": "resolver inconsistencias",
                    "reason": "Existen inconsistencias activas en el proyecto",
                    "impact": "alto"
                })

            if metrics["guardian"]["mode"] == "throttled":
                priorities.append({
                    "target": "optimizar uso de recursos",
                    "reason": "Guardian fue throttled recientemente",
                    "impact": "medio"
                })

            if metrics["project"]["files_total"] == 0:
                priorities.append({
                    "target": "escaneo inicial del proyecto",
                    "reason": "No hay archivos registrados aún",
                    "impact": "bajo"
                })

        decision = {
            "timestamp": datetime.utcnow().isoformat(),
            "priorities": priorities,
            "based_on": "system_metrics",
        }

        history.append(decision)
        self.memory._memory["evolution_decisions"] = history
        self.memory._persist()

        return decision