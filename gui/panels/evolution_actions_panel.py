# gui/panels/evolution_actions_panel.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from execution.evolution_pipeline import apply_evolution


class EvolutionActionsPanel(tk.Frame):
    def __init__(self, parent, memory):
        super().__init__(parent)
        self.memory = memory
        self._build()

    def _build(self):
        tk.Label(self, text="Evoluciones Preparadas").pack()

        for proposal in self.memory.get("proposed_connections") or []:
            if proposal.get("status") == "prepared":
                btn = tk.Button(
                    self,
                    text=f"Aplicar: {proposal['title']}",
                    command=lambda p=proposal: self._apply(p)
                )
                btn.pack(fill="x")

    def _apply(self, proposal):
        pwd = simpledialog.askstring(
            "Confirmación",
            "Contraseña:",
            show="*"
        )
        if not pwd:
            return

        try:
            apply_evolution(self.memory, proposal, pwd)
            messagebox.showinfo("Éxito", "Evolución aplicada")
        except Exception as e:
            messagebox.showerror("Error", str(e))