import tkinter as tk


class CognitiveDependenciesPanel(tk.Frame):
    """
    Visualiza dependencias entre conceptos cognitivos.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory
        self._build()
        self.after(3000, self.refresh)

    def _build(self):
        tk.Label(
            self,
            text="🔍 Dependencias Cognitivas",
            bg="#1e1e1e",
            fg="#ffb74d",
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

        deps = (
            self.memory._memory
            .get("cognitive_memory", {})
            .get("concept_dependencies", [])
        )

        if not deps:
            self.text.insert("end", "— No hay dependencias registradas\n")
        else:
            for d in deps:
                self.text.insert(
                    "end",
                    f"Concepto: {d.get('concept')}\n"
                    f"Depende de: {d.get('depends_on')}\n"
                    f"Estado: {'bloqueado' if d.get('blocked') else 'libre'}\n\n"
                )

        self.text.config(state="disabled")
        self.after(3000, self.refresh)