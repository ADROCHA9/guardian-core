# security/root_protection/root_watcher.py
import time
from security.identity_manager import is_identity_verified


def watch_root(memory, interval: float = 2.0):
    """
    Bloquea o libera el root SOLO según identidad sellada.
    """

    while True:
        if not is_identity_verified(memory):
            memory.update_guardian_state({
                "status": "locked",
                "ready_for_execution": False
            })
        else:
            # 🔒 Si ya está verificada, NO tocar más
            pass

        time.sleep(interval)