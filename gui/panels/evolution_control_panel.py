import tkinter as tk
from tkinter import messagebox


class EvolutionControlPanel(tk.Frame):
    """
    Panel central de control de evolución cognitiva de Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(2000, self.refresh)

    # =================================================
    def _build(self):
        tk.Label(
            self,
            text="🧠 Control de Evolución de Guardian",
            bg="#1e1e1e",
            fg="#00e5ff",
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            bg="#1e1e1e",
            fg="#cccccc",
            state="disabled",
            wrap="word",
            height=28
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=6)

        self.button_frame = tk.Frame(self, bg="#1e1e1e")
        self.button_frame.pack(fill="x", padx=10, pady=4)

    # =================================================
    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        guardian = self.memory._memory.get("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        # ---- Estado general ----
        self.text.insert("end", "📊 ESTADO GENERAL\n")
        self.text.insert("end", f"- Modo: {guardian.get('mode')}\n")

        paused = guardian.get("evolution_paused")
        if paused:
            self.text.insert("end", f"- Evolución pausada: {paused.get('reason')}\n")
        else:
            self.text.insert("end", "- Evolución activa\n")

        # ---- Prioridad Python ----
        self.text.insert("end", "\n🐍 PRIORIDAD PYTHON\n")
        self.text.insert(
            "end",
            f"- Conocimientos Python: {len(cognitive.get('python_knowledge', {}))}\n"
        )

        # ---- Etapas desbloqueadas ----
        self.text.insert("end", "\n🔓 ETAPAS DESBLOQUEADAS\n")
        for stage in guardian.get("unlocked_stages", []):
            self.text.insert("end", f"✓ {stage}\n")

        # ---- Propuestas ----
        self.text.insert("end", "\n📦 PROPUESTAS ACTIVAS\n")
        proposals = cognitive.get("structural_proposals", [])
        if not proposals:
            self.text.insert("end", "— No hay propuestas\n")
        else:
            for p in proposals[-5:]:
                self.text.insert(
                    "end",
                    f"- {p.get('proposal')} (riesgo {p.get('risk')})\n"
                )

        # ---- Permisos pendientes ----
        self.text.insert("end", "\n🔐 PERMISOS PENDIENTES\n")
        self._render_permissions()

        self.text.config(state="disabled")
        self.after(2000, self.refresh)

    # =================================================
    def _render_permissions(self):
        for w in self.button_frame.winfo_children():
            w.destroy()

        guardian = self.memory._memory.get("guardian_self", {})
        pending = guardian.get("pending_permissions", [])

        if not pending:
            self.text.insert("end", "— No hay permisos pendientes\n")
            return

        for i, p in enumerate(pending):
            self.text.insert(
                "end",
                f"[{i}] Acción: {p['action']}\n"
                f"    Motivo: {p['justification']}\n"
            )

            tk.Button(
                self.button_frame,
                text=f"✓ Aprobar {i}",
                command=lambda idx=i: self._approve(idx)
            ).pack(side="left", padx=4)

            tk.Button(
                self.button_frame,
                text=f"✗ Rechazar {i}",
                command=lambda idx=i: self._reject(idx)
            ).pack(side="left", padx=4)

    # =================================================
    def _approve(self, idx):
        try:
            self.memory._memory["guardian_self"]["pending_permissions"][idx]["status"] = "approved"
            self.memory._persist()
            messagebox.showinfo("Permiso", "Permiso aprobado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _reject(self, idx):
        try:
            self.memory._memory["guardian_self"]["pending_permissions"][idx]["status"] = "rejected"
            self.memory._persist()
            messagebox.showinfo("Permiso", "Permiso rechazado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))