import tkinter as tk


class EvolutionTimelinePanel(tk.Frame):
    """
    Muestra la línea de tiempo completa de la evolución de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="📈 Timeline de Evolución",
            bg="#1e1e1e",
            fg="#81c784",
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            bg="#1e1e1e",
            fg="#cccccc",
            state="disabled",
            height=30,
            wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=6)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        events = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("events", [])
        )

        if not events:
            self.text.insert("end", "— No hay eventos registrados\n")
        else:
            for e in events[-30:]:
                self.text.insert(
                    "end",
                    f"🕒 {e.get('timestamp')}\n"
                    f"Evento: {e.get('event')}\n"
                    f"Resumen: {e.get('summary')}\n\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)