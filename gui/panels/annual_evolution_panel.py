import tkinter as tk
from datetime import datetime


class AnnualEvolutionPanel(tk.Frame):
    """
    Vista anual comparativa del aprendizaje del Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        tk.Label(
            self,
            text="📈 Evolución Anual",
            bg="#1e1e1e",
            fg="#5cd65c",
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.canvas = tk.Canvas(
            self,
            height=220,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(5000, self.refresh)

    def refresh(self):
        self.canvas.delete("all")

        cognitive = self.memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {})
        daily = metrics.get("daily", {})

        if not daily:
            self.after(5000, self.refresh)
            return

        # últimos 365 días
        data = list(daily.items())[-365:]
        max_val = max(v.get("concepts_used", 0) for _, v in data) or 1

        w = self.canvas.winfo_width() or 600
        h = 200
        step = w / max(len(data), 1)

        for i, (_, v) in enumerate(data):
            val = v.get("concepts_used", 0)
            bar_h = int((val / max_val) * h)

            x0 = i * step
            self.canvas.create_rectangle(
                x0, h - bar_h, x0 + step, h,
                fill="#4da6ff",
                outline=""
            )

        self.after(5000, self.refresh)