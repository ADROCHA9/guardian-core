# environment/usb_detector.py
import platform
import time
from typing import List, Dict

def _list_usb_windows() -> List[Dict]:
    try:
        import win32api
        import win32file
    except ImportError:
        return []

    drives = []
    bitmask = win32api.GetLogicalDrives()
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if bitmask & 1:
            path = f"{letter}:\\"
            try:
                if win32file.GetDriveType(path) == win32file.DRIVE_REMOVABLE:
                    drives.append({"mount": path, "type": "removable"})
            except Exception:
                pass
        bitmask >>= 1
    return drives

def _list_usb_linux() -> List[Dict]:
    import os
    mounts = []
    for base in ("/media", "/mnt", "/run/media"):
        if os.path.isdir(base):
            for root, dirs, _ in os.walk(base):
                for d in dirs:
                    mounts.append({"mount": os.path.join(root, d), "type": "removable"})
                break
    return mounts

def list_usb_devices() -> List[Dict]:
    system = platform.system()
    if system == "Windows":
        return _list_usb_windows()
    if system == "Linux":
        return _list_usb_linux()
    return []

def watch_usb(poll_seconds: float = 2.0):
    """Generador de eventos pasivos: inserted/removed."""
    prev = set(d["mount"] for d in list_usb_devices())
    while True:
        time.sleep(poll_seconds)
        curr = set(d["mount"] for d in list_usb_devices())
        inserted = curr - prev
        removed = prev - curr
        for m in inserted:
            yield {"event": "usb_inserted", "mount": m}
        for m in removed:
            yield {"event": "usb_removed", "mount": m}
        prev = curr