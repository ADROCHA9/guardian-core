import tkinter as tk
from datetime import datetime, timedelta


class WeeklyComparisonPanel(tk.Frame):
    """
    Comparativa real entre semanas.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        tk.Label(
            self,
            text="📊 Comparativa Semanal",
            bg="#1e1e1e",
            fg="#4da6ff",
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            height=16,
            bg="#1e1e1e",
            fg="#cccccc",
            state="disabled",
            wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(5000, self.refresh)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        cognitive = self.memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {})
        daily = metrics.get("daily", {})

        if not daily:
            self.text.insert("end", "No hay datos suficientes aún.\n")
            self.text.config(state="disabled")
            self.after(5000, self.refresh)
            return

        dates = sorted(daily.keys())
        weeks = {}

        for d in dates:
            week = d[:7]  # YYYY-MM
            weeks.setdefault(week, 0)
            weeks[week] += daily[d].get("concepts_used", 0)

        weeks_list = list(weeks.items())[-2:]

        if len(weeks_list) < 2:
            self.text.insert("end", "Se necesitan al menos 2 semanas.\n")
        else:
            (w1, v1), (w2, v2) = weeks_list
            delta = v2 - v1

            self.text.insert(
                "end",
                f"Semana {w1}: {v1} conceptos\n"
                f"Semana {w2}: {v2} conceptos\n\n"
                f"Cambio: {delta:+d} conceptos\n"
            )

            if delta > 0:
                self.text.insert("end", "📈 Progreso acelerado\n")
            elif delta < 0:
                self.text.insert("end", "📉 Posible regresión\n")
            else:
                self.text.insert("end", "➖ Estancamiento\n")

        self.text.config(state="disabled")
        self.after(5000, self.refresh)