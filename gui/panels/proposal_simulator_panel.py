import tkinter as tk


class ProposalSimulatorPanel(tk.Frame):
    """
    Simula el impacto de propuestas antes de aprobarlas.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🧪 Simulador de Propuestas",
            bg="#1e1e1e",
            fg="#a5d6a7",
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

        proposals = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("module_refactor_proposals", {})
            .get("proposals", [])
        )

        if not proposals:
            self.text.insert("end", "— No hay propuestas activas\n")
        else:
            for p in proposals:
                self.text.insert(
                    "end",
                    f"Acción: {p['action']}\n"
                    f"Ruta: {p['path']}\n"
                    f"Motivo: {p['reason']}\n"
                    f"Impacto estimado: mejora estructural / riesgo bajo\n\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)