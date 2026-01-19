import tkinter as tk


class DecisionReplayPanel(tk.Frame):
    """
    Permite revisar decisiones pasadas de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🧠 Replay de Decisiones",
            bg="#1e1e1e",
            fg="#64b5f6",
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

        decisions = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("decisions", [])
        )

        if not decisions:
            self.text.insert("end", "— No hay decisiones registradas\n")
        else:
            for d in decisions[-15:]:
                self.text.insert(
                    "end",
                    f"🕒 {d.get('timestamp')}\n"
                    f"Decisión: {d.get('decision')}\n"
                    f"Resumen: {d.get('summary')}\n\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)