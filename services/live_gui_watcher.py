import os
import time
import threading


class LiveGuiWatcher(threading.Thread):
    """
    Observa cambios en archivos GUI y notifica al layout para recargar vistas.
    """

    def __init__(self, root_path, on_change, interval=1.0):
        super().__init__(daemon=True)
        self.root_path = root_path
        self.on_change = on_change
        self.interval = interval
        self._last_state = {}

    def run(self):
        while True:
            try:
                self._scan()
            except Exception:
                pass
            time.sleep(self.interval)

    def _scan(self):
        for root, _, files in os.walk(os.path.join(self.root_path, "gui")):
            for f in files:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(root, f)
                mtime = os.path.getmtime(path)

                if path not in self._last_state:
                    self._last_state[path] = mtime
                    continue

                if self._last_state[path] != mtime:
                    self._last_state[path] = mtime
                    self.on_change(path)