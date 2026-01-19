from datetime import datetime


class EvolutionControlCoreTask:
    """
    Controla qué capacidades están desbloqueadas según el nivel real.
    """

    STAGES = [
        "python_basic",
        "python_intermediate",
        "python_advanced",
        "micro_tests",
        "reflection",
        "module_creation",
        "self_modification",
        "gui_creation"
    ]

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        unlocked = guardian.get("unlocked_stages", ["python_basic"])

        python_knowledge = cognitive.get("python_knowledge", {})
        concepts = cognitive.get("concepts", {})

        # ---- reglas de desbloqueo ----
        if (
            "python_basic" in unlocked
            and "functions" in python_knowledge
            and "loops" in python_knowledge
            and "python_intermediate" not in unlocked
        ):
            unlocked.append("python_intermediate")

        if (
            "python_intermediate" in unlocked
            and len(python_knowledge) >= 15
            and "python_advanced" not in unlocked
        ):
            unlocked.append("python_advanced")

        if (
            "python_advanced" in unlocked
            and len(concepts) >= 10
            and "micro_tests" not in unlocked
        ):
            unlocked.append("micro_tests")

        if (
            "micro_tests" in unlocked
            and "reflection" not in unlocked
        ):
            unlocked.append("reflection")

        guardian["unlocked_stages"] = unlocked
        guardian["last_evolution_check"] = datetime.utcnow().isoformat()

        self.memory.log_event(
            event="evolution_stage_update",
            summary=f"Etapas desbloqueadas: {unlocked}"
        )
        self.memory._persist()

        return unlocked