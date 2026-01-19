import tkinter as tk
import math


class CognitiveDependenciesCanvasPanel(tk.Frame):
    """
    Visualización gráfica de dependencias cognitivas.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self.canvas = tk.Canvas(self, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.after(3000, self.refresh)

    def refresh(self):
        self.canvas.delete("all")

        deps = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("concept_dependencies", [])
        )

        if not deps:
            self.canvas.create_text(
                200, 200,
                text="No hay dependencias cognitivas",
                fill="#cccccc",
                font=("Consolas", 12)
            )
            self.after(3000, self.refresh)
            return

        concepts = list(
            {d["concept"] for d in deps} |
            {d["depends_on"] for d in deps}
        )

        center_x, center_y = 400, 300
        radius = 200
        positions = {}

        for i, c in enumerate(concepts):
            angle = 2 * math.pi * i / len(concepts)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[c] = (x, y)

            self.canvas.create_oval(
                x - 30, y - 30, x + 30, y + 30,
                outline="#64b5f6"
            )
            self.canvas.create_text(
                x, y,
                text=c,
                fill="#ffffff",
                font=("Consolas", 9)
            )

        for d in deps:
            x1, y1 = positions[d["depends_on"]]
            x2, y2 = positions[d["concept"]]

            self.canvas.create_line(
                x1, y1, x2, y2,
                arrow=tk.LAST,
                fill="#ff8a65"
            )

        self.after(3000, self.refresh)