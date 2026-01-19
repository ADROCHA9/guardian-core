from config.runtime_profile import RUNTIME_PROFILE, SERVER_PROFILE


class CognitiveOrchestrator:
    """
    Decide SI Guardian debe pensar.
    En server-only: SIEMPRE piensa.
    """

    def __init__(self, memory, throttle):
        self.memory = memory
        self.throttle = throttle

    def should_think(self) -> bool:
        # 🔥 SERVER: nunca bloquear cognición
        if RUNTIME_PROFILE == "server":
            return True

        # DESKTOP: lógica original
        return self.throttle.allow_thinking()

    def thinking_mode(self, ram_usage: float) -> str:
        """
        Decide intensidad, NO apagado.
        """
        if RUNTIME_PROFILE == "server":
            if ram_usage < SERVER_PROFILE["max_ram_tolerance"]:
                return "aggressive"
            return "light"

        # Desktop legacy
        if ram_usage < 0.85:
            return "normal"
        if ram_usage < 0.95:
            return "light"
        return "micro"