# gui/animation_engine.py
import time

class AnimationEngine:
    def __init__(self, root, fps=30):
        self.root = root
        self.callbacks = []
        self.interval = int(1000 / fps)
        self._running = False

    def add(self, callback):
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def start(self):
        if not self._running:
            self._running = True
            self._tick()

    def _tick(self):
        if not self._running:
            return

        for cb in self.callbacks:
            try:
                cb(self.interval / 1000)
            except Exception:
                pass

        self.root.after(self.interval, self._tick)