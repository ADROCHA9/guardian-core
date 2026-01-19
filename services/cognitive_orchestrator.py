import time
import psutil
from config.runtime_profile import SERVER_PROFILE


class CognitiveOrchestrator:
    """
    Decide CUÁNDO Guardian puede pensar.
    En server: agresivo pero autorregulado.
    """

    def __init__(self, memory, throttle):
        self.memory = memory
        self.throttle = throttle
        self.last_think = None

    def should_think(self) -> bool:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        free_ram_mb = psutil.virtual_memory().available / 1024 / 1024

        if cpu > SERVER_PROFILE["max_cpu_percent"]:
            return False

        if ram > SERVER_PROFILE["max_ram_percent"]:
            return False

        if free_ram_mb < SERVER_PROFILE["min_free_ram_mb"]:
            return False

        now = time.time()

        # Pensamiento forzado periódico (CLAVE)
        if self.last_think is None:
            self.last_think = now
            return True

        if now - self.last_think >= SERVER_PROFILE["force_think_interval"]:
            self.last_think = now
            return True

        self.last_think = now
        return True
