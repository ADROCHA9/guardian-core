# services/system_throttle.py

import psutil
import time


class SystemThrottle:
    """
    Controla si el sistema está en condiciones de pensar.
    Guardian se adapta al hardware, no al revés.
    """

    def __init__(
        self,
        max_cpu: float = 60.0,
        max_ram: float = 80.0,
        cooldown_seconds: int = 10
    ):
        self.max_cpu = max_cpu
        self.max_ram = max_ram
        self.cooldown_seconds = cooldown_seconds
        self._last_block = 0.0

    def allow_thinking(self) -> bool:
        """
        Retorna True si Guardian puede pensar.
        False si debe entrar en modo pasivo.
        """
        now = time.time()

        # Evita checkear demasiado seguido
        if now - self._last_block < self.cooldown_seconds:
            return False

        cpu = psutil.cpu_percent(interval=0.2)
        ram = psutil.virtual_memory().percent

        if cpu > self.max_cpu or ram > self.max_ram:
            self._last_block = now
            return False

        return True

    def snapshot(self) -> dict:
        """
        Métricas rápidas para debugging.
        """
        vm = psutil.virtual_memory()
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "ram_percent": vm.percent,
            "ram_available_mb": round(vm.available / 1024 / 1024, 1)
        }