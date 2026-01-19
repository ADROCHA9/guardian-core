import tkinter as tk


class IntegrityPanel(tk.Frame):
    """
    Muestra el estado de integridad de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🛡 Estado de Integridad",
            bg="#1e1e1e",
            fg="#81c784",
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.label = tk.Label(
            self,
            text="",
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Consolas", 11)
        )
        self.label.pack(padx=10, pady=20)

    def refresh(self):
        guardian = self.memory._memory.get("guardian_self", {})
        healthy = (
            not guardian.get("evolution_paused") and
            guardian.get("root_locked") and
            guardian.get("unlocked_stages")
        )

        self.label.config(
            text="🟢 Guardian íntegro y operativo"
            if healthy else
            "🟠 Atención: revisar estado interno"
        )

        self.after(3000, self.refresh)