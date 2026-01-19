import tkinter as tk
from datetime import datetime


class EvolutionPanel(tk.Frame):
    """
    Evolución diaria / semanal / mensual del Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        self.mode = "daily"  # daily | weekly | monthly

        top = tk.Frame(self, bg="#1e1e1e")
        top.pack(fill="x")

        for m in ("daily", "weekly", "monthly"):
            tk.Button(top, text=m.capitalize(), command=lambda x=m: self.set_mode(x)).pack(side="left")

        self.canvas = tk.Canvas(self, height=160, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(3000, self.refresh)

    def set_mode(self, mode):
        self.mode = mode

    def refresh(self):
        self.canvas.delete("all")

        cognitive = self.memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {})
        daily = metrics.get("daily", {})

        if not daily:
            self.after(3000, self.refresh)
            return

        data = list(daily.items())

        if self.mode == "weekly":
            data = data[-7:]
        elif self.mode == "monthly":
            data = data[-30:]

        max_val = max(v["concepts_used"] for _, v in data) or 1

        w = self.canvas.winfo_width() or 400
        h = 140
        step = w / max(len(data), 1)

        for i, (_, v) in enumerate(data):
            bar = int((v["concepts_used"] / max_val) * h)
            x0 = i * step + 5
            self.canvas.create_rectangle(x0, h - bar, x0 + step - 4, h, fill="#5cd65c", outline="")

        self.after(3000, self.refresh)