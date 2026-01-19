# services/usb_node_manager.py
import os

VACCINE_FILE = "guardian_node.activate"


def detect_usb_node(mount_path, memory):
    """
    Detecta activación manual del Guardian en otro hardware.
    """
    marker = os.path.join(mount_path, VACCINE_FILE)

    if os.path.exists(marker):
        memory.log_event(
            event="remote_node_activated",
            summary=f"Nodo activado en {mount_path}"
        )

        memory._memory.setdefault("nodes", []).append({
            "path": mount_path,
            "status": "linked"
        })
        memory._persist()