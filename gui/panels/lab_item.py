# gui/panels/lab_item.py
import tkinter as tk
from gui.theme import THEME


class LabItem(tk.Frame):
    """
    Representa una propuesta individual del Guardian.
    """

    def __init__(self, parent, memory, proposal: dict):
        super().__init__(parent, bg=THEME["bg"], bd=1, relief="solid")
        self.memory = memory
        self.proposal = proposal

        self._build()

    def _build(self):
        title = self.proposal.get("description", "Propuesta sin descripción")
        priority = self.proposal.get("priority", "normal").upper()
        origin = self.proposal.get("origin", "guardian")

        header = tk.Label(
            self,
            text=f"{title}",
            bg=THEME["bg"],
            fg=THEME["text_main"],
            font=THEME["font_main"],
            wraplength=800,
            justify="left"
        )
        header.pack(anchor="w", padx=6, pady=4)

        meta = tk.Label(
            self,
            text=f"Origen: {origin} | Prioridad: {priority}",
            bg=THEME["bg"],
            fg=THEME["text_dim"],
            font=THEME["font_small"]
        )
        meta.pack(anchor="w", padx=6, pady=(0, 4))