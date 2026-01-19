import tkinter as tk
from services.idea_negotiation_task import IdeaNegotiationTask


class GuidedSuggestionsPanel(tk.Frame):
    """
    Permite sugerencias cognitivas guiadas hacia Guardian,
    con negociación real y criterio evolutivo.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self.negotiator = IdeaNegotiationTask(memory)

        self._build()

    def _build(self):
        tk.Label(
            self,
            text="🎯 Sugerencias guiadas a Guardian",
            bg="#1e1e1e",
            fg="#5cd65c",
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=10, pady=6)

        self.entry = tk.Text(
            self,
            height=4,
            wrap="word",
            bg="#111111",
            fg="#ffffff",
            insertbackground="#5cd65c"
        )
        self.entry.pack(fill="x", padx=10, pady=6)

        tk.Button(
            self,
            text="Enviar sugerencia",
            command=self.send
        ).pack(anchor="e", padx=10, pady=4)

        self.feedback = tk.Text(
            self,
            height=10,
            wrap="word",
            bg="#0d0d0d",
            fg="#cccccc",
            state="disabled"
        )
        self.feedback.pack(fill="both", expand=True, padx=10, pady=6)

    # =================================================
    # ENVÍO DE SUGERENCIA
    # =================================================
    def send(self):
        text = self.entry.get("1.0", "end").strip()
        if not text:
            return

        self.entry.delete("1.0", "end")

        # Ejecutar negociación cognitiva real
        try:
            result = self.negotiator.negotiate(text)
        except Exception as e:
            self._append_feedback(
                f"❌ Error al negociar sugerencia:\n{e}\n"
            )
            return

        # Registrar intención y resultado
        guardian = self.memory._memory.setdefault("guardian_self", {})
        guardian["last_guided_suggestion"] = {
            "goal": text,
            "decision": result.get("decision"),
            "confidence": result.get("confidence"),
            "reason": result.get("reason")
        }

        self.memory.log_event(
            event="guided_suggestion_negotiated",
            summary=(
                f"Sugerencia: {text} | "
                f"Decisión: {result.get('decision')}"
            )
        )
        self.memory._persist()

        # Feedback visual
        self._append_feedback(
            "🧠 Guardian respondió:\n"
            f"- Decisión: {result.get('decision')}\n"
            f"- Confianza: {result.get('confidence')}\n"
            f"- Motivo: {result.get('reason')}\n\n"
        )

    # =================================================
    # FEEDBACK
    # =================================================
    def _append_feedback(self, text: str):
        self.feedback.config(state="normal")
        self.feedback.insert("end", text)
        self.feedback.see("end")
        self.feedback.config(state="disabled")