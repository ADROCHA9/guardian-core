import tkinter as tk
from gui.theme import THEME


class ProjectManagerPanel(tk.Frame):
    """
    Panel de gestión de proyectos + navegación.
    """

    def __init__(self, parent, memory, on_project_selected, on_view_change):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self.on_project_selected = on_project_selected
        self.on_view_change = on_view_change
        self._build()

    def _build(self):
        # ---------- Título ----------
        tk.Label(
            self,
            text="📁 Proyectos",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        ).pack(anchor="w", padx=10, pady=8)

        # ---------- Navegación ----------
        nav = tk.Frame(self, bg=THEME["panel_bg"])
        nav.pack(fill="x", padx=8, pady=4)

        # === VISTAS REGISTRADAS EN MAIN LAYOUT ===
        views = [
            ("core", "🧠 Núcleo"),
            ("lab", "🧪 Laboratorio"),
            ("environment", "🌍 Entorno"),
            ("nodes", "🔌 Nodos"),
            ("security", "🔐 Seguridad"),

            # --- Evolución / Cognición ---
            ("evolution", "🧬 Evolución"),
            ("activity", "⚙️ Actividad"),
            ("annual_evolution", "📈 Evolución anual"),
            ("weekly_comparison", "📊 Comparativa semanal"),
            ("metrics", "📊 Métricas"),
            ("metrics_dashboard", "📊 Dashboard"),

            # --- Inteligencia / Planificación ---
            ("heuristics", "🧠 Heurísticas"),
            ("guided_suggestions", "🎯 Sugerencias"),
            ("guardian_plans", "🤖 Planes de Guardian"),
            ("evolution_control", "🧠 Control Evolución"),

            # --- Memoria / Razonamiento ---
            ("memory_inspector", "🧠 Memoria"),
            ("mind_versions", "📊 Versiones Mentales"),
            ("internal_reasoning", "🧠 Razonamiento"),
            ("decision_replay", "🧠 Replay"),
            ("evolution_timeline", "📈 Timeline"),

            # --- Propuestas / Permisos ---
            ("proposals", "📦 Propuestas"),
            ("proposal_simulator", "🧪 Simulador"),
            ("advanced_permissions", "🎛 Permisos"),

            # --- Dependencias / Errores ---
            ("error_patterns", "🔍 Patrones de error"),
            ("error_monitor", "🚨 Errores"),
            ("cognitive_dependencies", "🔍 Dependencias"),
            ("dependencies_graph", "🧠 Dependencias (Gráfico)"),

            # --- Soporte ---
            ("gui_hints", "🧩 GUI Hints"),
            ("history", "📜 Historial"),
            ("integrity", "🛡 Integridad"),
        ]

        for name, label in views:
            tk.Button(
                nav,
                text=label,
                command=lambda n=name: self.on_view_change(n)
            ).pack(fill="x", pady=2)

        # ---------- Lista de proyectos ----------
        self.listbox = tk.Listbox(
            self,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            selectbackground=THEME["accent"],
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(fill="both", expand=True, padx=10, pady=6)

        self._ensure_projects()
        self._load_projects()

        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    # =================================================
    # PROYECTOS
    # =================================================
    def _ensure_projects(self):
        if self.memory.get("projects") is None:
            active = self.memory.get("project")
            self.memory._memory["projects"] = [active] if active else []
            self.memory._persist()

    def _load_projects(self):
        self.listbox.delete(0, "end")
        for p in self.memory.get("projects", []):
            self.listbox.insert("end", p.get("name", "Proyecto"))

    def _on_select(self, _):
        sel = self.listbox.curselection()
        if not sel:
            return
        project = self.memory.get("projects", [])[sel[0]]
        self.on_project_selected(project)