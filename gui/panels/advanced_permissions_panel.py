import tkinter as tk
from tkinter import messagebox


class AdvancedPermissionsPanel(tk.Frame):
    """
    Panel avanzado para gestionar permisos humanos de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(2000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🎛 Permisos Humanos (Avanzado)",
            bg="#1e1e1e",
            fg="#ffcc80",
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

        self.buttons = tk.Frame(self, bg="#1e1e1e")
        self.buttons.pack(fill="x", padx=10, pady=4)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        for w in self.buttons.winfo_children():
            w.destroy()

        guardian = self.memory._memory.get("guardian_self", {})
        permissions = guardian.get("pending_permissions", [])

        if not permissions:
            self.text.insert("end", "— No hay permisos registrados\n")
        else:
            for i, p in enumerate(permissions):
                self.text.insert(
                    "end",
                    f"[{i}] Acción: {p.get('action')}\n"
                    f"    Motivo: {p.get('justification')}\n"
                    f"    Estado: {p.get('status')}\n"
                    f"    Resultado: {p.get('execution_result', 'N/A')}\n\n"
                )

                if p.get("status") == "pending":
                    tk.Button(
                        self.buttons,
                        text=f"✓ Aprobar {i}",
                        command=lambda idx=i: self._set_status(idx, "approved")
                    ).pack(side="left", padx=4)

                    tk.Button(
                        self.buttons,
                        text=f"✗ Rechazar {i}",
                        command=lambda idx=i: self._set_status(idx, "rejected")
                    ).pack(side="left", padx=4)

                    tk.Button(
                        self.buttons,
                        text=f"⛔ Revocar {i}",
                        command=lambda idx=i: self._revoke(idx)
                    ).pack(side="left", padx=4)

        self.text.config(state="disabled")
        self.after(2000, self.refresh)

    def _set_status(self, idx, status):
        try:
            self.memory._memory["guardian_self"]["pending_permissions"][idx]["status"] = status
            self.memory._persist()
            messagebox.showinfo("Permisos", f"Permiso {status}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _revoke(self, idx):
        try:
            del self.memory._memory["guardian_self"]["pending_permissions"][idx]
            self.memory._persist()
            messagebox.showinfo("Permisos", "Permiso revocado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))