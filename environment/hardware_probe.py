# environment/hardware_probe.py
import psutil
import platform

def cpu_info() -> dict:
    return {
        "cores_logical": psutil.cpu_count(logical=True),
        "cores_physical": psutil.cpu_count(logical=False),
        "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
        "usage_percent": psutil.cpu_percent(interval=0.5),
    }

def memory_info() -> dict:
    mem = psutil.virtual_memory()
    return mem._asdict()

def disk_info() -> dict:
    return {
        "partitions": [p._asdict() for p in psutil.disk_partitions(all=False)],
        "usage": psutil.disk_usage("/")._asdict() if platform.system() != "Windows"
                 else psutil.disk_usage("C:\\")._asdict(),
    }

def hardware_snapshot() -> dict:
    return {
        "cpu": cpu_info(),
        "memory": memory_info(),
        "disk": disk_info(),
        "platform": platform.machine(),
    }