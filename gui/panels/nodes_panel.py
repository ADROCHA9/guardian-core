# gui/panels/nodes_panel.py
import tkinter as tk
from gui.theme import THEME

class NodesPanel(tk.Frame):
    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory

        self.label = tk.Label(
            self,
            text="Nodos",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        self.label.pack(anchor="w", padx=8, pady=4)

        self.content = tk.Label(
            self,
            text="",
            bg=THEME["panel_bg"],
            fg=THEME["text_main"],
            font=THEME["font_main"],
            justify="left"
        )
        self.content.pack(anchor="w", padx=8, pady=4)

    def update(self, dt):
        nodes = self.memory.get("nodes") or {}
        count = len(nodes)
        self.content.config(text=f"Nodos registrados: {count}")