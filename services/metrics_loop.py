# services/metrics_loop.py
import time
import threading
from metrics.system_metrics import collect_metrics


class MetricsLoop:
    """
    Recalcula métricas del sistema periódicamente.
    """

    def __init__(self, memory, interval=5):
        self.memory = memory
        self.interval = interval
        self._running = False

    def start(self):
        if self._running:
            return

        self._running = True
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

        self.memory.log_event(
            event="metrics_loop_started",
            summary=f"Métricas activas (intervalo {self.interval}s)"
        )

    def _run(self):
        while self._running:
            try:
                metrics = collect_metrics(self.memory)
                self.memory._memory["metrics"] = metrics
                self.memory._persist()
            except Exception as e:
                self.memory.log_event(
                    event="metrics_error",
                    summary=str(e)
                )

            time.sleep(self.interval)