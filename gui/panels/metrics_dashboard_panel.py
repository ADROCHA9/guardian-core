import tkinter as tk


class MetricsDashboardPanel(tk.Frame):
    """
    Dashboard en tiempo real de métricas cognitivas.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(2000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="📊 Dashboard Cognitivo",
            bg="#1e1e1e",
            fg="#4dd0e1",
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

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        guardian = self.memory._memory.get("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        self.text.insert("end", "📈 MÉTRICAS ACTUALES\n\n")

        self.text.insert("end", f"- Dependencia humana: {guardian.get('human_dependency')}\n")
        self.text.insert("end", f"- Etapas desbloqueadas: {guardian.get('unlocked_stages')}\n")
        self.text.insert("end", f"- Evolución pausada: {bool(guardian.get('evolution_paused'))}\n")

        self.text.insert("end", "\n🧠 CONOCIMIENTO\n")
        self.text.insert("end", f"- Conceptos: {len(cognitive.get('concepts', {}))}\n")
        self.text.insert("end", f"- Patrones de error: {len(cognitive.get('error_patterns', []))}\n")

        self.text.config(state="disabled")
        self.after(2000, self.refresh)