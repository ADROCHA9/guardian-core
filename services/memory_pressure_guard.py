import psutil
import time

class MemoryPressureGuard:
    """
    Protege al sistema ante presión extrema de RAM.
    """

    LOW_RAM_MB = 500      # alerta
    CRITICAL_RAM_MB = 200 # supervivencia

    def __init__(self, memory):
        self.memory = memory

    def check(self):
        vm = psutil.virtual_memory()
        available_mb = vm.available / (1024 * 1024)

        guardian = self.memory._memory.setdefault("guardian_self", {})

        if available_mb < self.CRITICAL_RAM_MB:
            guardian["memory_mode"] = "survival"
            return "survival"

        if available_mb < self.LOW_RAM_MB:
            guardian["memory_mode"] = "conservative"
            return "conservative"

        guardian["memory_mode"] = "normal"
        return "normal"