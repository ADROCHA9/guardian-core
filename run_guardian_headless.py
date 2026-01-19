#!/usr/bin/env python3
import time
import signal
import sys
import os

from services.continuous_work_loop import ContinuousWorkLoop
from memory import ProjectMemory


def main():
    # Root del proyecto
    root_path = os.path.abspath(os.path.dirname(__file__))

    # Inicializar memoria
    memory = ProjectMemory(root_path)
    memory.load()

    # Inicializar loop cognitivo
    loop = ContinuousWorkLoop(memory)
    loop.start()

    # Manejo limpio de señales (systemd)
    def shutdown_handler(signum, frame):
        try:
            memory._memory.setdefault("guardian_self", {})["last_shutdown_ts"] = time.time()
            memory._persist()
        finally:
            sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    # 🔒 BLOQUEO PRINCIPAL (CRÍTICO PARA systemd)
    # Este loop mantiene vivo el proceso principal
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
