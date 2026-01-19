# environment/os_probe.py
import platform
import os

def detect_os() -> dict:
    system = platform.system()
    release = platform.release()
    version = platform.version()

    return {
        "system": system,
        "release": release,
        "version": version,
        "is_windows": system == "Windows",
        "is_linux": system == "Linux",
        "is_macos": system == "Darwin",
    }

def os_present() -> bool:
    # Si hay filesystem típico de OS, asumimos modo usuario
    return any([
        os.path.exists("C:\\Windows"),
        os.path.exists("/bin"),
        os.path.exists("/usr"),
    ])
