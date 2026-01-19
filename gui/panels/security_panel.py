# gui/panels/security_panel.py
import tkinter as tk
from gui.theme import THEME

class SecurityPanel(tk.Frame):
    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory

        self.label = tk.Label(
            self,
            text="Seguridad",
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
        issues = self.memory.get("inconsistencies") or []
        level = "OK" if not issues else "RIESGO"
        color = THEME["accent"] if not issues else THEME["warning"]

        self.content.config(
            text=f"Estado: {level}\nAlertas: {len(issues)}",
            fg=color
        )