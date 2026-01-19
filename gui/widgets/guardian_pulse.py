# gui/widgets/guardian_pulse.py
import tkinter as tk
import math
from gui.theme import THEME


class GuardianPulse(tk.Canvas):
    def __init__(self, parent, memory, width=400, height=120):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=THEME["panel_bg"],
            highlightthickness=0
        )
        self.memory = memory
        self.width = width
        self.height = height

        self.t = 0.0
        self.speed = 1.0
        self.points = []
        self.max_points = width

        self._init_baseline()

    def _init_baseline(self):
        self.points = [(x, self.height // 2) for x in range(self.width)]

    def _derive_frequency(self) -> float:
        guardian = self.memory.get("guardian_self") or {}
        inconsistencies = self.memory.get("inconsistencies") or []

        status = guardian.get("status", "stable")
        base = 1.0

        if status == "stable":
            base = 1.0
        elif status == "warning":
            base = 1.6
        elif status == "critical":
            base = 2.2

        # inconsistencias aceleran el pulso
        base += min(len(inconsistencies) * 0.1, 1.0)
        return base

    def update(self, dt):
        self.speed = self._derive_frequency()
        self.t += dt * self.speed * 6.0

        # Generación ECG simple: pico + retorno
        y = self.height // 2
        phase = self.t % (2 * math.pi)

        if 0.1 < phase < 0.2:
            y -= 30
        elif 0.2 <= phase < 0.3:
            y += 20

        self.points.append((self.points[-1][0] + 1, y))
        if len(self.points) > self.max_points:
            self.points.pop(0)

        self._redraw()

    def _redraw(self):
        self.delete("all")
        shifted = [
            (i, p[1]) for i, p in enumerate(self.points)
        ]
        self.create_line(
            shifted,
            fill=THEME["accent"],
            width=2,
            smooth=True
        )
