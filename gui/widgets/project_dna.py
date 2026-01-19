# gui/widgets/project_dna.py
import tkinter as tk
import math
from gui.theme import THEME


class ProjectDNA(tk.Canvas):
    """
    ADN del Proyecto.
    Representa módulos, relaciones y coherencia estructural.
    """

    def __init__(self, parent, memory, width=500, height=200):
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
        self.speed = 0.6

        self.center_y = height // 2
        self.radius = 55
        self.turns = 5
        self.points_per_turn = 24

    def _project_metrics(self):
        files = self.memory.get("files") or {}
        relations = self.memory.get("relations") or []
        inconsistencies = self.memory.get("inconsistencies") or []

        return {
            "files": len(files),
            "relations": len(relations),
            "inconsistencies": len(inconsistencies)
        }

    def _coherence_ratio(self, metrics):
        if metrics["files"] == 0:
            return 0.0
        return max(
            0.0,
            1.0 - (metrics["inconsistencies"] / metrics["files"])
        )

    def update(self, dt):
        self.t += dt * self.speed
        self.delete("all")

        metrics = self._project_metrics()
        coherence = self._coherence_ratio(metrics)

        # Color según coherencia
        if coherence > 0.85:
            color = THEME["accent"]
        elif coherence > 0.6:
            color = THEME["warning"]
        else:
            color = THEME["danger"]

        x_step = self.width / (self.turns * self.points_per_turn)

        for i in range(self.turns * self.points_per_turn):
            phase = self.t + (i / 5.0)
            x = i * x_step

            y1 = self.center_y + math.sin(phase) * self.radius
            y2 = self.center_y + math.sin(phase + math.pi) * self.radius

            self.create_oval(
                x - 2, y1 - 2, x + 2, y1 + 2,
                fill=color,
                outline=""
            )
            self.create_oval(
                x - 2, y2 - 2, x + 2, y2 + 2,
                fill=color,
                outline=""
            )

            if i % 5 == 0:
                self.create_line(
                    x, y1, x, y2,
                    fill=color,
                    width=1
                )