import tkinter as tk

from gui.theme import THEME


class CognitiveMetricsPanel(tk.Frame):
    """
    Panel de métricas cognitivas del Guardian.
    Vista READ-ONLY del estado vivo del sistema.
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
            text="📊 Métricas Cognitivas",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        header.pack(anchor="w", padx=10, pady=6)

        self.text = tk.Text(
            self,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            state="disabled",
            wrap="word",
            height=24
        )
        self.text.pack(fill="both", expand=True, padx=10, pady=6)

        refresh_btn = tk.Button(
            self,
            text="Actualizar métricas",
            command=self._refresh
        )
        refresh_btn.pack(anchor="e", padx=10, pady=6)

    # =================================================
    # DATA
    # =================================================
    def _refresh(self):
        m = self.memory._memory

        guardian = m.get("guardian_self", {})
        identity = m.get("identity", {})
        services = m.get("services", {})
        root = m.get("guardian_root", {})
        proposals = m.get("proposed_connections", [])
        intents = m.get("open_questions", [])

        # Conteos de propuestas
        status_count = {}
        for p in proposals:
            status = p.get("status", "unknown")
            status_count[status] = status_count.get(status, 0) + 1

        lines = [
            "🧠 ESTADO COGNITIVO",
            f"- Estado: {guardian.get('status')}",
            f"- Último ciclo: {guardian.get('last_cycle')}",
            f"- Nivel de evolución: {guardian.get('evolution_level')}",
            f"- Identidad verificada: {guardian.get('identity_verified')}",
            "",
            "🔄 ACTIVIDAD DEL SISTEMA",
            f"- Servicios activos: {', '.join(k for k, v in services.items() if v == 'active')}",
            f"- Trabajo continuo: {services.get('continuous_work')}",
            f"- Intenciones humanas pendientes: {len([i for i in intents if i.get('status') == 'new'])}",
            "",
            "📦 PROPUESTAS",
            f"- Total: {len(proposals)}",
        ]

        for status, count in status_count.items():
            lines.append(f"  • {status}: {count}")

        lines.extend([
            "",
            "🔐 SEGURIDAD",
            f"- Operador: {identity.get('operator')}",
            f"- Root protegido: {root.get('protected')}",
            f"- Root bloqueado: {root.get('locked')}",
            "",
            "🧪 EVOLUCIÓN",
            f"- Propuestas aprobadas: {status_count.get('approved', 0)}",
            f"- Propuestas integradas: {status_count.get('integrated', 0)}",
            f"- Propuestas rechazadas: {status_count.get('rejected', 0)}",
        ])

        self._set_text("\n".join(lines))

    # =================================================
    # UTIL
    # =================================================
    def _set_text(self, text: str):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", text)
        self.text.config(state="disabled")