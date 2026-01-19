# gui/panels/gui_hints_panel.py

import tkinter as tk
from gui.theme import THEME


class GuiHintsPanel(tk.Frame):
    """
    Panel simple de visualización de GUI Hints.
    READ-ONLY. No ejecuta acciones.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self._build()
        self._refresh()

    # =================================================
    # UI
    # =================================================
    def _build(self):
        header = tk.Label(
            self,
            text="🧩 GUI Hints (Intención Cognitiva)",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        header.pack(anchor="w", padx=10, pady=6)

        self.listbox = tk.Listbox(
            self,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            height=12
        )
        self.listbox.pack(fill="both", expand=True, padx=10, pady=6)

        refresh_btn = tk.Button(
            self,
            text="Actualizar",
            command=self._refresh
        )
        refresh_btn.pack(anchor="e", padx=10, pady=6)

    # =================================================
    # DATA
    # =================================================
    def _refresh(self):
        self.listbox.delete(0, "end")

        cm = self.memory._memory.get("cognitive_memory", {})
        hints = cm.get("gui_hints", [])

        if not hints:
            self.listbox.insert("end", "— No hay GUI hints aún —")
            return

        for i, h in enumerate(hints[-20:]):
            desc = f"{h.get('type', 'hint')} → {h.get('target', 'module')}"
            loc = h.get("location") or h.get("interaction", "")
            self.listbox.insert(
                "end",
                f"#{i} | {desc} | {loc}"
            )