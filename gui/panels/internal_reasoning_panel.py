import tkinter as tk


class InternalReasoningPanel(tk.Frame):
    """
    Muestra razonamiento interno de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(2000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🧠 Razonamiento Interno",
            bg="#1e1e1e",
            fg="#81d4fa",
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

        guardian = self.memory._memory.get("guardian_self", {})

        keys = [
            "learning_intent_justification",
            "strategy_change_explanations",
            "autonomy_explanation",
            "evolution_paused",
        ]

        for k in keys:
            if k in guardian:
                self.text.insert("end", f"{k}:\n{guardian[k]}\n\n")

        self.text.config(state="disabled")
        self.after(2000, self.refresh)