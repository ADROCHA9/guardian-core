from datetime import datetime


class AdaptiveModuleEvolutionTask:
    """
    Evoluciona la complejidad de módulos y tests
    según el nivel cognitivo real de Guardian.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        concepts = cognitive.get("concepts", {})
        level_sum = sum(c.get("level", 0) for c in concepts.values())

        tier = (
            "basic" if level_sum < 20 else
            "intermediate" if level_sum < 50 else
            "advanced"
        )

        evolution = guardian.get("module_evolution", {})
        last_tier = evolution.get("tier")

        if last_tier == tier:
            return None

        evolution.update({
            "tier": tier,
            "updated_at": datetime.utcnow().isoformat(),
            "description": (
                "Módulos simples y tests básicos" if tier == "basic" else
                "Módulos compuestos y tests con estado" if tier == "intermediate" else
                "Módulos reutilizables y tests multi-escenario"
            )
        })

        guardian["module_evolution"] = evolution

        self.memory.log_event(
            event="module_evolution_updated",
            summary=f"Evolución de módulos → nivel {tier}"
        )
        self.memory._persist()

        return evolution