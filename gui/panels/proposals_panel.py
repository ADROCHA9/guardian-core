# gui/panels/proposals_panel.py

import tkinter as tk
from tkinter import messagebox

from gui.theme import THEME

from services.execution_planner import ExecutionPlanner
from services.adaptive_intelligence import AdaptiveIntelligence
from services.ethical_explainer import EthicalExplainer
from services.execution_transition import can_execute_proposal
from execution.evolution_pipeline import apply_evolution


class ProposalsPanel(tk.Frame):
    """
    Panel cognitivo final:
    Estrategia + Adaptación + Ética + Ejecución controlada.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self.exec = ExecutionPlanner(memory)
        self.ai = AdaptiveIntelligence(memory)
        self.ethics = EthicalExplainer(memory)
        self._build()

    # =================================================
    # UI
    # =================================================
    def _build(self):
        tk.Label(
            self,
            text="🧠 Gobernanza Cognitiva y Ética",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        ).pack(anchor="w", padx=10, pady=6)

        self.output = tk.Text(
            self,
            height=24,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            state="disabled",
            wrap="word"
        )
        self.output.pack(fill="both", expand=True, padx=10, pady=6)

        btns = tk.Frame(self, bg=THEME["panel_bg"])
        btns.pack(fill="x", padx=10, pady=6)

        # -------- BOTONES DE GOBERNANZA --------
        tk.Button(
            btns,
            text="🧠 Explicar aprendizaje",
            command=self._explain
        ).pack(side="left", padx=4)

        tk.Button(
            btns,
            text="🔍 Detectar sesgos",
            command=self._bias
        ).pack(side="left", padx=4)

        tk.Button(
            btns,
            text="📜 Auditoría ética",
            command=self._audit
        ).pack(side="left", padx=4)

        # -------- BOTONES DE FLUJO REAL --------
        tk.Button(
            btns,
            text="✅ Aprobar propuesta",
            command=self._approve_selected
        ).pack(side="right", padx=4)

        tk.Button(
            btns,
            text="▶️ Ejecutar propuesta aprobada",
            fg="white",
            bg="#27ae60",
            command=self._execute_selected
        ).pack(side="right", padx=4)

    # =================================================
    # ACCIONES COGNITIVAS
    # =================================================
    def _explain(self):
        self._set(self.ethics.explain_learning())

    def _bias(self):
        lines = self.ethics.detect_biases()
        self._set("\n".join(lines))

    def _audit(self):
        self._set(self.ethics.ethical_audit())

    # =================================================
    # FLUJO DE PROPUESTAS
    # =================================================
    def _approve_selected(self):
        proposals = self.memory.get("proposed_connections", [])
        if not proposals:
            messagebox.showwarning("Propuestas", "No hay propuestas disponibles.")
            return

        proposal = proposals[-1]

        if proposal.get("status") != "prepared":
            messagebox.showwarning(
                "Propuesta",
                "La propuesta debe estar en estado PREPARED."
            )
            return

        if not messagebox.askyesno(
            "Confirmar aprobación",
            "¿Aprobar esta propuesta para ejecución real?\n\n"
            "⚠️ Esto NO ejecuta aún."
        ):
            return

        proposal["status"] = "approved"
        self.memory.log_event(
            event="proposal_approved",
            summary=proposal.get("description", "sin descripción")
        )
        self.memory._persist()

        messagebox.showinfo(
            "Aprobada",
            "Propuesta aprobada correctamente.\nLista para ejecución."
        )

    def _execute_selected(self):
        proposals = self.memory.get("proposed_connections", [])
        if not proposals:
            messagebox.showwarning("Propuestas", "No hay propuestas disponibles.")
            return

        proposal = proposals[-1]

        if not can_execute_proposal(proposal, self.memory):
            messagebox.showerror(
                "Ejecución bloqueada",
                "La propuesta no cumple las condiciones de ejecución."
            )
            return

        if not messagebox.askyesno(
            "⚠️ Confirmación final",
            "¿EJECUTAR esta propuesta en el proyecto real?\n\n"
            "✔ Sandbox validado\n"
            "✔ Tests ejecutados\n"
            "✔ Cambios reversibles\n\n"
            "Esta acción modifica archivos reales."
        ):
            return

        try:
            apply_evolution(self.memory, proposal, password=None)
            proposal["status"] = "executed"

            self.memory.log_event(
                event="proposal_executed",
                summary=proposal.get("description", "sin descripción")
            )
            self.memory._persist()

            messagebox.showinfo(
                "Ejecución completa",
                "La propuesta fue ejecutada correctamente."
            )

        except Exception as e:
            messagebox.showerror("Error de ejecución", str(e))

    # =================================================
    # UTIL
    # =================================================
    def _set(self, text: str):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.config(state="disabled")