import tkinter as tk


class HeuristicsPanel(tk.Frame):
    """
    Muestra heurísticas activas que el Guardian usa para decidir.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        tk.Label(
            self,
            text="🧠 Heurísticas activas",
            bg="#1e1e1e",
            fg="#ffa500",
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

        self.after(3000, self.refresh)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        cognitive = self.memory.get("cognitive_memory", {})
        heuristics = cognitive.get("error_heuristics", [])

        if not heuristics:
            self.text.insert("end", "No hay heurísticas activas aún.\n")
        else:
            for h in heuristics:
                if not h.get("active", True):
                    continue
                self.text.insert(
                    "end",
                    f"- Si ocurre [{h.get('when_error_type')}]: "
                    f"{h.get('suggestion')}\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)