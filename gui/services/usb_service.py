# services/usb_service.py
from environment.usb_detector import watch_usb


def run_usb_service(memory):
    for evt in watch_usb():
        memory.log_event(
            event=evt["event"],
            summary=f"USB detectado: {evt['mount']}"
        )