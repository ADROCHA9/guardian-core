import time
import threading

from services.system_throttle import SystemThrottle
from services.cognitive_orchestrator import CognitiveOrchestrator
from config.runtime_profile import RUNTIME_PROFILE, SERVER_PROFILE


class ContinuousWorkLoop:
    """
    Loop cognitivo PERPETUO.

    Principio:
    - NO ejecuta tareas individuales
    - NO decide capacidades
    - SOLO garantiza que Guardian piense SIEMPRE
    """

    BASE_INTERVAL_DESKTOP = 15
    PASSIVE_INTERVAL_DESKTOP = 180

    def __init__(self, guardian_core, interval: int = None):
        # guardian_core ES la instancia única de GuardianCognitiveCore
        self.brain = guardian_core
        self.memory = guardian_core.memory

        self._running = False

        self.throttle = SystemThrottle()
        self.orchestrator = CognitiveOrchestrator(self.memory, self.throttle)

        # Configuración por entorno
        if RUNTIME_PROFILE == "server":
            self.interval = 5
            self.passive_interval = SERVER_PROFILE["passive_learning_interval"]
        else:
            self.interval = interval or self.BASE_INTERVAL_DESKTOP
            self.passive_interval = self.PASSIVE_INTERVAL_DESKTOP

    # =================================================
    # CONTROL
    # =================================================
    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._running = False

    # =================================================
    # LOOP PRINCIPAL
    # =================================================
    def _run(self):
        while self._running:
            cycle_start = time.time()
            try:
                self._cycle()
            except Exception:
                # Guardian JAMÁS se cae
                pass

            elapsed = time.time() - cycle_start
            time.sleep(max(1.0, self.interval - elapsed))

    # =================================================
    # CICLO ÚNICO
    # =================================================
    def _cycle(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        now = time.time()

        # -------------------------------
        # HEARTBEAT REAL (vida)
        # -------------------------------
        guardian["alive"] = True
        guardian["heartbeat"] = guardian.get("heartbeat", 0) + 1
        guardian["last_heartbeat_ts"] = now

        # -------------------------------
        # PAUSA MANUAL
        # -------------------------------
        if guardian.get("paused"):
            guardian["last_skip_reason"] = "paused"
            self.memory._persist()
            time.sleep(5)
            return

        # -------------------------------
        # ORQUESTACIÓN (NUNCA BLOQUEA EN SERVER)
        # -------------------------------
        if not self.orchestrator.should_think():
            guardian["last_skip_reason"] = "orchestrator"
            self.memory._persist()
            time.sleep(2)
            return

        # -------------------------------
        # EJECUCIÓN COGNITIVA ÚNICA
        # -------------------------------
        guardian["mode"] = "thinking"
        guardian["learning_state"] = "active"
        guardian["last_cycle"] = time.time()

        # 🔥 TODA la inteligencia vive acá
        self.brain.think(human_input=None)

        self.memory._persist()
