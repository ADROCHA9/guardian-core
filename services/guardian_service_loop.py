# services/guardian_service_loop.py
import threading
import time

from services.continuous_work_loop import ContinuousWorkLoop
from services.evolution_orchestrator import evolve
from services.metrics_loop import MetricsLoop
from services.memory_cleaner import clean_memory

from security.root_protection.root_resolver import resolve_guardian_root
from security.root_protection.root_watcher import watch_root
from security.identity_manager import is_identity_verified


def start_services(memory):
    """
    Inicia servicios del Guardian.
    RESPETA identidad persistente.
    NO modifica identidad.
    """

    memory._memory.setdefault("services", {})

    # ================= ROOT PROTECTION =================
    root = resolve_guardian_root()
    memory._memory["guardian_root"] = {
        "path": root,
        "protected": True,
        "watch_mode": "active"
    }
    memory._persist()

    # Root watcher (solo observa)
    threading.Thread(
        target=watch_root,
        args=(memory,),
        daemon=True
    ).start()

    # ================= SERVICIOS CONDICIONALES =================

    def guarded_start():
        """
        Espera identidad verificada antes de iniciar loops cognitivos.
        """
        while not is_identity_verified(memory):
            time.sleep(1)

        # CONTINUOUS THINKING
        ContinuousWorkLoop(memory, interval=15).start()

        # METRICS
        MetricsLoop(memory, interval=5).start()

        # MEMORY CLEANER (NO toca identidad)
        def cleaner_loop():
            while True:
                clean_memory(memory)
                time.sleep(60)

        threading.Thread(target=cleaner_loop, daemon=True).start()

        # EVOLUTION ORCHESTRATOR
        def evolution_loop():
            while True:
                evolve(memory)
                time.sleep(30)

        threading.Thread(target=evolution_loop, daemon=True).start()

        memory._memory["services"].update({
            "continuous_work": "active",
            "metrics": "active",
            "evolution": "active",
            "memory_cleaner": "active"
        })
        memory._persist()

    # Lanzar arranque protegido
    threading.Thread(target=guarded_start, daemon=True).start()