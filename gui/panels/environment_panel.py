# gui/panels/environment_panel.py
import tkinter as tk
from gui.theme import THEME

class EnvironmentPanel(tk.Frame):
    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory

        self.label = tk.Label(
            self,
            text="Entorno",
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
        env = self.memory.get("environment") or {}
        mode = env.get("mode", {}).get("mode", "UNKNOWN")
        os_info = env.get("os", {}).get("system", "N/A")
        hw = env.get("hardware", {}).get("cpu", {})

        text = (
            f"Modo: {mode}\n"
            f"OS: {os_info}\n"
            f"CPU cores: {hw.get('cores_logical', '?')}"
        )
        self.content.config(text=text)