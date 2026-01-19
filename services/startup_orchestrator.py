# services/startup_orchestrator.py

import threading
import time


class StartupOrchestrator:
    """
    Arranque por fases para evitar picos de CPU/RAM.
    """

    def __init__(self, memory, services: dict):
        """
        services = {
            "metrics": metrics_loop.start,
            "continuous_work": continuous_work.start,
            "evolution": evolution.start,
        }
        """
        self.memory = memory
        self.services = services

    def start(self):
        # Fase 1: Sistema mínimo (inmediato)
        self._log("Startup fase 1: núcleo y GUI")
        time.sleep(0.5)

        # Fase 2: Métricas (ligero)
        self._delayed_start("metrics", delay=5)

        # Fase 3: Orquestación cognitiva
        self._delayed_start("continuous_work", delay=10)

        # Fase 4: Evolución (lo más pesado)
        self._delayed_start("evolution", delay=15)

    def _delayed_start(self, name: str, delay: int):
        if name not in self.services:
            return

        def _run():
            time.sleep(delay)
            self._log(f"Startup fase: {name}")
            try:
                self.services[name]()
            except Exception as e:
                self._log(f"Error iniciando {name}: {e}")

        threading.Thread(target=_run, daemon=True).start()

    def _log(self, msg: str):
        self.memory.log_event(
            event="startup_phase",
            summary=msg
        )
        self.memory._persist()