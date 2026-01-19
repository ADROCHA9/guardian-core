# gui/widgets/guardian_dna.py
import tkinter as tk
import math
from gui.theme import THEME


class GuardianDNA(tk.Canvas):
    """
    ADN del Guardian.
    Representa capacidades, permisos y nivel evolutivo.
    """

    def __init__(self, parent, memory, width=400, height=180):
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

        self.center_y = height // 2
        self.radius = 40
        self.turns = 6
        self.points_per_turn = 20

    def _get_capabilities(self):
        return self.memory.get("capabilities") or {}

    def _get_evolution_level(self):
        guardian = self.memory.get("guardian_self") or {}
        return guardian.get("evolution_level", 0)

    def update(self, dt):
        self.t += dt * self.speed
        self.delete("all")

        caps = self._get_capabilities()
        level = self._get_evolution_level()

        total_segments = max(len(caps), 1)
        active_segments = sum(
            1 for c in caps.values() if c
        )

        # Color según madurez
        color_active = THEME["accent"]
        color_inactive = THEME["text_dim"]

        x_step = self.width / (self.turns * self.points_per_turn)

        idx = 0
        for turn in range(self.turns * self.points_per_turn):
            phase = self.t + (turn / 6.0)
            x = turn * x_step

            y1 = self.center_y + math.sin(phase) * self.radius
            y2 = self.center_y + math.sin(phase + math.pi) * self.radius

            # Activación progresiva según nivel
            active = idx < active_segments + level

            self.create_oval(
                x - 2, y1 - 2, x + 2, y1 + 2,
                fill=color_active if active else color_inactive,
                outline=""
            )
            self.create_oval(
                x - 2, y2 - 2, x + 2, y2 + 2,
                fill=color_active if active else color_inactive,
                outline=""
            )

            # Unión (escalera ADN)
            if turn % 4 == 0:
                self.create_line(
                    x, y1, x, y2,
                    fill=color_active if active else color_inactive,
                    width=1
                )

            idx = (idx + 1) % max(total_segments, 1)