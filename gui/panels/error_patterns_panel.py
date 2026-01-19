import tkinter as tk


class ErrorPatternsPanel(tk.Frame):
    """
    Muestra patrones de error detectados por Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        tk.Label(
            self,
            text="🔍 Patrones de error detectados",
            bg="#1e1e1e",
            fg="#ff4d4d",
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
        patterns = cognitive.get("error_patterns", [])
        heuristics = {
            h.get("when_error_type"): h.get("suggestion")
            for h in cognitive.get("error_heuristics", [])
        }

        if not patterns:
            self.text.insert("end", "Aún no se detectaron patrones de error.\n")
        else:
            for p in patterns:
                status = "ACTIVO" if p.get("active") else "DECAÍDO"
                suggestion = heuristics.get(p.get("type"), "—")

                self.text.insert(
                    "end",
                    f"• Tipo: {p.get('type')}\n"
                    f"  Ocurrencias: {p.get('occurrences')}\n"
                    f"  Estado: {status}\n"
                    f"  Regla: {suggestion}\n\n"
                )

        self.text.config(state="disabled")
        self.after(4000, self.refresh)