import time
import threading

from services.guardian_cognitive_core import GuardianCognitiveCore
from services.system_throttle import SystemThrottle
from services.cognitive_orchestrator import CognitiveOrchestrator
from config.runtime_profile import RUNTIME_PROFILE, SERVER_PROFILE


class ContinuousWorkLoop:
    """
    Loop cognitivo perpetuo (server-safe).
    """

    BASE_INTERVAL_DESKTOP = 15
    PASSIVE_INTERVAL_DESKTOP = 180

    def __init__(self, memory, interval: int = None):
        self.memory = memory
        self._running = False

        self.throttle = SystemThrottle()
        self.orchestrator = CognitiveOrchestrator(memory, self.throttle)
        self.brain = GuardianCognitiveCore(memory)

        if RUNTIME_PROFILE == "server":
            self.interval = 5
            self.passive_interval = SERVER_PROFILE["passive_learning_interval"]
        else:
            self.interval = interval or self.BASE_INTERVAL_DESKTOP
            self.passive_interval = self.PASSIVE_INTERVAL_DESKTOP

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self._running = False

    def _run(self):
        while self._running:
            start = time.time()
            try:
                self._cycle()
            except Exception as e:
                # Guardian NUNCA muere
                self.memory.log_event(
                    "runtime_exception",
                    str(e)
                )

            elapsed = time.time() - start
            time.sleep(max(1.0, self.interval - elapsed))

    def _cycle(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        now = time.time()

        guardian["alive"] = True
        guardian["heartbeat"] = guardian.get("heartbeat", 0) + 1
        guardian["last_heartbeat_ts"] = now

        if guardian.get("paused"):
            guardian["last_skip_reason"] = "paused"
            self.memory._persist()
            time.sleep(5)
            return

        if not self.orchestrator.should_think():
            guardian["last_skip_reason"] = "orchestrator"
            self.memory._persist()
            time.sleep(2)
            return

        guardian["mode"] = "thinking"
        guardian["learning_state"] = "active"
        guardian["last_cycle"] = now

        self.brain.think(human_input=None)
        self.memory._persist()
