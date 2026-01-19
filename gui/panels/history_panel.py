import tkinter as tk
from tkinter import messagebox

from gui.theme import THEME
from services.integration_manager import IntegrationManager


class HistoryPanel(tk.Frame):
    """
    Panel de historial y rollback del Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self.manager = IntegrationManager(memory)
        self._build()
        self._refresh()

    # =================================================
    # UI
    # =================================================
    def _build(self):
        header = tk.Label(
            self,
            text="📜 Historial y Rollback",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        header.pack(anchor="w", padx=10, pady=4)

        self.listbox = tk.Listbox(
            self,
            height=10,
            bg=THEME["bg"],
            fg=THEME["text_main"]
        )
        self.listbox.pack(fill="x", padx=10, pady=4)

        btn_frame = tk.Frame(self, bg=THEME["panel_bg"])
        btn_frame.pack(fill="x", padx=10, pady=4)

        refresh_btn = tk.Button(
            btn_frame,
            text="Actualizar historial",
            command=self._refresh
        )
        refresh_btn.pack(side="left")

        rollback_btn = tk.Button(
            btn_frame,
            text="Rollback al estado seleccionado",
            fg="white",
            bg="#c0392b",
            command=self._rollback
        )
        rollback_btn.pack(side="right")

    # =================================================
    # LÓGICA
    # =================================================
    def _refresh(self):
        self.listbox.delete(0, "end")
        backups = self.memory.get("backups") or []

        if not backups:
            self.listbox.insert("end", "— No hay backups registrados —")
            return

        for i, b in enumerate(backups):
            self.listbox.insert(
                "end",
                f"#{i} — {b.get('timestamp')}"
            )

    def _rollback(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "Rollback",
                "Seleccioná un estado para restaurar."
            )
            return

        index = selection[0]

        confirm = messagebox.askyesno(
            "Confirmar rollback",
            f"¿Querés volver al estado #{index}?\n\n"
            "⚠️ Se perderán los cambios posteriores."
        )

        if not confirm:
            return

        result = self.manager.rollback_to(index)

        messagebox.showinfo("Rollback", result)
        self._refresh()