from services.strategy_engine import StrategyEngine
from services.integration_manager import IntegrationManager


class ExecutionPlanner:
    """
    Planificador ejecutivo del Guardian.
    Ejecuta SOLO roadmaps aprobados por humano.
    """

    def __init__(self, memory):
        self.memory = memory
        self.strategy = StrategyEngine(memory)
        self.integrator = IntegrationManager(memory)

    # =================================================
    # ROADMAPS MÚLTIPLES
    # =================================================
    def generate_roadmaps(self):
        """
        Genera múltiples escenarios de roadmap.
        """
        base = self.strategy.plan_by_priority()

        by_priority = base
        by_reverse_priority = list(reversed(base))

        return {
            "por_prioridad": self._format(base),
            "prioridad_invertida": self._format(by_reverse_priority),
        }

    def _format(self, proposals):
        return [
            {
                "proposal_id": p["id"],
                "priority": p.get("priority"),
                "description": p.get("description"),
            }
            for p in proposals
        ]

    # =================================================
    # RESOLUCIÓN AUTOMÁTICA DE CONFLICTOS (PROPUESTA)
    # =================================================
    def propose_conflict_resolution(self):
        conflicts = self.strategy.detect_conflicts()
        resolutions = []

        for c in conflicts:
            resolutions.append({
                "conflict": c,
                "action": "adjust_priority",
                "details": (
                    f"Bajar prioridad de {c['b']} "
                    f"para resolver conflicto con {c['a']}"
                )
            })

        return resolutions

    def apply_conflict_resolution(self, resolution):
        """
        Aplica una resolución SOLO si el humano lo confirma.
        """
        conflict = resolution["conflict"]
        b_id = conflict["b"]

        proposals = self.memory.get("proposed_connections", [])
        for p in proposals:
            if p["id"] == b_id:
                p["priority"] = (p.get("priority") or 5) + 1

        self.memory.log_event(
            event="conflict_resolved_automatically",
            summary=resolution["details"]
        )
        self.memory._persist()

    # =================================================
    # EJECUCIÓN DE ROADMAP
    # =================================================
    def execute_roadmap(self, roadmap):
        """
        Ejecuta un roadmap aprobado paso a paso.
        """
        for step in roadmap:
            pid = step["proposal_id"]
            proposal = next(
                (p for p in self.memory.get("proposed_connections", [])
                 if p["id"] == pid and p.get("status") == "approved"),
                None
            )

            if not proposal:
                continue

            result = self.integrator.apply_approved()
            if "❌" in result:
                return result

        return "✅ Roadmap ejecutado correctamente."