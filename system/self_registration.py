# system/self_registration.py
import os
import json
import platform
from system.icon_manager import ensure_guardian_icon


def get_guardian_state_dir() -> str:
    home = os.path.expanduser("~")
    path = os.path.join(home, ".guardian")
    os.makedirs(path, exist_ok=True)
    return path


def register_guardian_root(root_path: str):
    """
    Registra (o actualiza) la ubicación real del Guardian.
    """
    state_dir = get_guardian_state_dir()
    state_file = os.path.join(state_dir, "guardian_path.json")

    data = {
        "root_path": root_path,
        "os": platform.system()
    }

    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Crear / actualizar icono y acceso
    ensure_guardian_icon(root_path, state_dir)