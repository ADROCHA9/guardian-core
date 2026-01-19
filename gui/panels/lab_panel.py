import tkinter as tk
from gui.theme import THEME
from gui.panels.lab_item import LabItem


class LabPanel(tk.Frame):
    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self.items = []
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="🧪 Laboratorio del Guardian",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        ).pack(anchor="w", padx=10, pady=6)

        self.container = tk.Frame(self, bg=THEME["panel_bg"])
        self.container.pack(fill="both", expand=True, padx=6, pady=6)

        self.log = tk.Text(
            self,
            height=6,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            state="disabled"
        )
        self.log.pack(fill="x", padx=6, pady=4)

    def update(self, dt=0):
        # Propuestas
        proposals = self.memory.get("proposed_connections", [])

        if len(proposals) != len(self.items):
            for i in self.items:
                i.destroy()
            self.items.clear()

            for p in proposals:
                item = LabItem(self.container, self.memory, p)
                item.pack(fill="x", pady=4)
                self.items.append(item)

        # Log reciente
        events = self.memory.get("evolution_log", [])[-5:]
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        for e in events:
            self.log.insert("end", f"{e['event']} — {e['summary']}\n")
        self.log.config(state="disabled")