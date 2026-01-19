# environment/environment_state.py
import platform
import psutil
import shutil
from datetime import datetime


def collect_environment_state() -> dict:
    """
    Detecta el entorno REAL donde corre Guardian.
    No ejecuta nada peligroso. Solo lectura.
    """

    # -------------------------
    # OS
    # -------------------------
    os_info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
    }

    # -------------------------
    # CPU
    # -------------------------
    cpu_info = {
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "frequency_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else None,
        "usage_percent": psutil.cpu_percent(interval=0.5),
    }

    # -------------------------
    # MEMORIA
    # -------------------------
    mem = psutil.virtual_memory()
    memory_info = {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "used_percent": mem.percent,
    }

    # -------------------------
    # DISCO
    # -------------------------
    disk = shutil.disk_usage("/")
    disk_info = {
        "total_gb": round(disk.total / (1024 ** 3), 2),
        "free_gb": round(disk.free / (1024 ** 3), 2),
    }

    # -------------------------
    # MODO OPERATIVO
    # -------------------------
    mode = {
        "mode": "desktop_os",
        "can_execute_sandbox": True,
        "can_manage_hardware": False,  # se habilita luego con consentimiento
    }

    return {
        "detected_at": datetime.utcnow().isoformat(),
        "os": os_info,
        "cpu": cpu_info,
        "memory": memory_info,
        "disk": disk_info,
        "mode": mode,
    }