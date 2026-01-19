import subprocess
import time
import psutil
import os
import sys
import signal
import logging
import atexit
import json
from logging.handlers import RotatingFileHandler
from datetime import datetime

# ================= CONFIG =================
GUARDIAN_ROOT = r"C:\Users\CONECTIA BA\guardian_bot"
HEADLESS_SCRIPT = "run_guardian_headless.py"
PROCESS_KEYWORD = "run_guardian_headless.py"
PYTHON_EXE = sys.executable

LOG_DIR = os.path.join(GUARDIAN_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "guardian_bootstrap.log")
STATE_FILE = os.path.join(LOG_DIR, "guardian_health.json")
LOCK_FILE = os.path.join(LOG_DIR, "bootstrap.lock")

MAX_LOG_SIZE = 2 * 1024 * 1024
BACKUP_COUNT = 5

WATCHDOG_INTERVAL = 30
STALL_THRESHOLD = 10 * 60
# =========================================


# ================= SINGLETON =================
if os.path.exists(LOCK_FILE):
    sys.exit(0)

with open(LOCK_FILE, "w") as f:
    f.write(str(os.getpid()))


def cleanup_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


atexit.register(cleanup_lock)
# ============================================


# ================= LOGGING =================
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("guardian_bootstrap")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=MAX_LOG_SIZE,
    backupCount=BACKUP_COUNT,
    encoding="utf-8"
)
handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)
logger.addHandler(handler)
# ==========================================


def guardian_pid():
    for p in psutil.process_iter(['pid', 'cmdline']):
        try:
            if PROCESS_KEYWORD in " ".join(p.info.get("cmdline") or []):
                return p.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def arrancar_guardian():
    script = os.path.join(GUARDIAN_ROOT, HEADLESS_SCRIPT)
    if not os.path.exists(script):
        logger.error("run_guardian_headless.py no encontrado")
        return False

    subprocess.Popen(
        [PYTHON_EXE, script],
        cwd=GUARDIAN_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    logger.info("Guardian iniciado (headless)")
    return True


def apagar_guardian():
    pid = guardian_pid()
    if not pid:
        return
    try:
        p = psutil.Process(pid)
        logger.info(f"Apagando Guardian (PID {pid})")
        p.terminate()
        p.wait(timeout=10)
        logger.info("Guardian apagado limpiamente")
    except Exception as e:
        logger.warning(f"Error apagando Guardian: {e}")


def evaluar_salud_cognitiva():
    memory_path = os.path.join(GUARDIAN_ROOT, "memory.json")
    if not os.path.exists(memory_path):
        return "UNKNOWN", "memory.json no encontrado"

    try:
        with open(memory_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return "UNKNOWN", "memoria ilegible"

    guardian = data.get("guardian_self", {})
    now = time.time()

    for key in ("last_cycle", "last_passive_learning"):
        ts = guardian.get(key)
        if not ts:
            continue
        try:
            if now - datetime.fromisoformat(ts).timestamp() < STALL_THRESHOLD:
                return "HEALTHY", "actividad cognitiva reciente"
        except Exception:
            pass

    return "IDLE", "sin actividad reciente"


def guardar_estado_salud(status, reason):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "checked_at": datetime.utcnow().isoformat(),
                "status": status,
                "reason": reason
            },
            f
        )


def watchdog_tick():
    pid = guardian_pid()

    if not pid:
        logger.warning("Guardian no está corriendo. Reiniciando…")
        arrancar_guardian()
        return

    # ---- control externo ----
    control_flag = os.path.join(GUARDIAN_ROOT, "guardian_control.flag")
    if os.path.exists(control_flag):
        with open(control_flag, "r") as f:
            cmd = f.read().strip()
        os.remove(control_flag)

        if cmd == "shutdown":
            apagar_guardian()
            return
        elif cmd == "restart":
            apagar_guardian()
            time.sleep(2)
            arrancar_guardian()

    status, reason = evaluar_salud_cognitiva()
    guardar_estado_salud(status, reason)

    if status == "HEALTHY":
        logger.info("Salud cognitiva: OK")
    elif status == "IDLE":
        logger.info("Guardian vivo (idle)")
    else:
        logger.warning(f"Salud cognitiva incierta: {reason}")


# ================= APAGADO SEGURO =================
def handle_exit(signum=None, frame=None):
    logger.info("Apagado del sistema detectado. Cerrando Guardian…")
    apagar_guardian()
    cleanup_lock()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
atexit.register(apagar_guardian)
# ==================================================


# ================= MAIN =================
if __name__ == "__main__":
    logger.info("Bootstrap Guardian activo")

    if not guardian_pid():
        arrancar_guardian()
        time.sleep(3)

    try:
        while True:
            watchdog_tick()
            time.sleep(WATCHDOG_INTERVAL)
    except KeyboardInterrupt:
        handle_exit()