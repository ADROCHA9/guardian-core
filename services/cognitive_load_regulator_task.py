class CognitiveLoadRegulatorTask:
    """
    Regula intensidad cognitiva usando:
    - tiempo de ciclo
    - errores
    - advertencias heurísticas
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self, cycle_time: float, active_tasks: int, error_count: int):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        window = guardian.setdefault("learning_window", {})

        # Heurísticas recientes
        cognitive = self.memory._memory.get("cognitive_memory", {})
        heuristics = cognitive.get("error_heuristics", [])

        active_heuristics = len([h for h in heuristics if h.get("active")])

        # 🔧 Decisión de intensidad
        if error_count > 0 or active_heuristics > 3:
            intensity = "focused"
        elif cycle_time < 0.05:
            intensity = "intensive"
        else:
            intensity = "adaptive"

        window["intensity"] = intensity
        self.memory._persist()
        return intensity