# gui/widgets/project_pulse.py
import tkinter as tk
import math
from gui.theme import THEME


class ProjectPulse(tk.Canvas):
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
        files = self.memory.get("files") or {}
        inconsistencies = self.memory.get("inconsistencies") or []
        project = self.memory.get("project") or {}

        # Base según tamaño del proyecto
        base = 0.8 + min(len(files) / 200.0, 1.2)

        # Cambios recientes aceleran
        if project.get("last_scan"):
            base += 0.3

        # Inconsistencias del proyecto alteran el pulso
        base += min(len(inconsistencies) * 0.08, 0.8)

        return base

    def update(self, dt):
        self.speed = self._derive_frequency()
        self.t += dt * self.speed * 6.0

        y = self.height // 2
        phase = self.t % (2 * math.pi)

        # ECG más suave que el Guardian
        if 0.15 < phase < 0.25:
            y -= 22
        elif 0.25 <= phase < 0.35:
            y += 14

        self.points.append((self.points[-1][0] + 1, y))
        if len(self.points) > self.max_points:
            self.points.pop(0)

        self._redraw()

    def _redraw(self):
        self.delete("all")
        shifted = [(i, p[1]) for i, p in enumerate(self.points)]
        self.create_line(
            shifted,
            fill=THEME["text_main"],
            width=2,
            smooth=True
        )