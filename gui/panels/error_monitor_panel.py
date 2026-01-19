import tkinter as tk


class ErrorMonitorPanel(tk.Frame):
    """
    Muestra errores detectados en todo el sistema Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(2000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🚨 Monitor de Errores",
            bg="#1e1e1e",
            fg="#ef5350",
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

        errors = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("errors", [])
        )

        if not errors:
            self.text.insert("end", "— No se detectaron errores\n")
        else:
            for e in errors[-10:]:
                self.text.insert(
                    "end",
                    f"📍 Origen: {e.get('source')}\n"
                    f"❌ Error: {e.get('error')}\n"
                    f"🧠 Posible solución: {e.get('suggested_fix', 'N/A')}\n\n"
                )

        self.text.config(state="disabled")
        self.after(2000, self.refresh)