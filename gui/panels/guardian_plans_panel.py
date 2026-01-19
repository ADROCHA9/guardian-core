import tkinter as tk


class GuardianPlansPanel(tk.Frame):
    """
    Muestra planes propuestos por Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        tk.Label(
            self,
            text="🤖 Planes propuestos por Guardian",
            bg="#1e1e1e",
            fg="#5cd65c",
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            height=18,
            bg="#1e1e1e",
            fg="#cccccc",
            state="disabled",
            wrap="word"
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(4000, self.refresh)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        cognitive = self.memory.get("cognitive_memory", {})
        plans = cognitive.get("proposed_plans", [])

        if not plans:
            self.text.insert(
                "end",
                "Guardian aún no ha propuesto planes.\n"
                "Esto ocurrirá cuando detecte patrones claros.\n"
            )
        else:
            for p in plans[-5:]:
                self.text.insert(
                    "end",
                    f"Objetivo: {p.get('goal')}\n"
                    f"Motivo: {p.get('reason')}\n"
                    f"Prioridad: {p.get('priority')}\n\n"
                )

        self.text.config(state="disabled")
        self.after(4000, self.refresh)