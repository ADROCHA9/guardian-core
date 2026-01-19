# services/service_loop.py
import threading
from services.usb_service import run_usb_service


class ServiceLoop:
    def __init__(self, memory):
        self.memory = memory
        self.threads = []

    def start(self):
        usb_thread = threading.Thread(
            target=run_usb_service,
            args=(self.memory,),
            daemon=True
        )
        usb_thread.start()
        self.threads.append(usb_thread)