import tkinter as tk


class MindVersionsPanel(tk.Frame):
    """
    Visualiza las versiones mentales de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="📊 Versiones Mentales",
            bg="#1e1e1e",
            fg="#ffd54f",
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            bg="#1e1e1e",
            fg="#cccccc",
            state="disabled",
            height=30
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=6)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        versions = self.memory._memory.get("guardian_self", {}).get("mind_versions", [])

        if not versions:
            self.text.insert("end", "— No hay versiones mentales aún\n")
        else:
            for i, v in enumerate(versions[-10:]):
                self.text.insert(
                    "end",
                    f"[{i}] Fecha: {v['created_at']}\n"
                    f"    Hash: {v['signature'][:12]}...\n"
                    f"    Snapshot: {v['snapshot']}\n\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)