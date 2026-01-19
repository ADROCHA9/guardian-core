import tkinter as tk
from gui.theme import THEME

from gui.core_view import CoreView
from gui.panels.lab_panel import LabPanel
from gui.panels.environment_panel import EnvironmentPanel
from gui.panels.nodes_panel import NodesPanel
from gui.panels.security_panel import SecurityPanel
from gui.panels.evolution_panel import EvolutionPanel
from gui.panels.project_manager_panel import ProjectManagerPanel
from gui.panels.communication_panel import CommunicationPanel
from gui.panels.history_panel import HistoryPanel
from gui.panels.gui_hints_panel import GuiHintsPanel

# === VISTAS AVANZADAS EXISTENTES ===
from gui.panels.memory_inspector_panel import MemoryInspectorPanel
from gui.panels.proposals_panel import ProposalsPanel
from gui.panels.metrics_panel import CognitiveMetricsPanel

# === NUEVAS VISTAS (JORNADA ACTUAL) ===
from gui.panels.activity_panel import ActivityPanel
from gui.panels.annual_evolution_panel import AnnualEvolutionPanel
from gui.panels.heuristics_panel import HeuristicsPanel
from gui.panels.guided_suggestions_panel import GuidedSuggestionsPanel
from gui.panels.error_patterns_panel import ErrorPatternsPanel
from gui.panels.weekly_comparison_panel import WeeklyComparisonPanel
from gui.panels.guardian_plans_panel import GuardianPlansPanel
from gui.panels.evolution_control_panel import EvolutionControlPanel
from gui.panels.mind_versions_panel import MindVersionsPanel
from gui.panels.internal_reasoning_panel import InternalReasoningPanel
from gui.panels.proposal_simulator_panel import ProposalSimulatorPanel
from gui.panels.error_monitor_panel import ErrorMonitorPanel
from gui.panels.cognitive_dependencies_panel import CognitiveDependenciesPanel
from gui.panels.decision_replay_panel import DecisionReplayPanel
from gui.panels.evolution_timeline_panel import EvolutionTimelinePanel
from gui.panels.advanced_permissions_panel import AdvancedPermissionsPanel
from gui.panels.cognitive_dependencies_canvas_panel import CognitiveDependenciesCanvasPanel
from gui.panels.metrics_dashboard_panel import MetricsDashboardPanel
from gui.panels.integrity_panel import IntegrityPanel

from services.encoding_guard import force_utf8
force_utf8()


class MainLayout(tk.Frame):
    """
    Layout principal del Guardian.

    Principio clave:
    - UI PASIVA
    - No ejecuta lógica cognitiva
    - Solo refleja estado real y permite control humano
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["bg"])
        self.memory = memory
        self.views = {}
        self._build()

    # =================================================
    # BUILD
    # =================================================
    def _build(self):
        # ================= TOP BAR =================
        top = tk.Frame(self, bg=THEME["panel_bg"], height=40)
        top.pack(fill="x")

        tk.Label(
            top,
            text="GUARDIAN — Control Central",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        ).pack(side="left", padx=10)

        # ================= BODY =================
        body = tk.Frame(self, bg=THEME["bg"])
        body.pack(fill="both", expand=True)

        # ================= LEFT (PROJECTS + NAV) =================
        left = tk.Frame(body, bg=THEME["panel_bg"], width=260)
        left.pack(side="left", fill="y")

        self.project_manager = ProjectManagerPanel(
            left,
            self.memory,
            on_project_selected=self._on_project_selected,
            on_view_change=self.show_view
        )
        self.project_manager.pack(fill="both", expand=True)

        # ================= CENTER (VIEWS) =================
        self.view_container = tk.Frame(body, bg=THEME["bg"])
        self.view_container.pack(side="left", fill="both", expand=True)

        # ================= REGISTRO DE VISTAS =================

        # --- CORE ---
        self.register_view("core", CoreView)
        self.register_view("lab", LabPanel)
        self.register_view("environment", EnvironmentPanel)
        self.register_view("nodes", NodesPanel)
        self.register_view("security", SecurityPanel)

        # --- COGNITIVO / EVOLUCIÓN ---
        self.register_view("evolution", EvolutionPanel)
        self.register_view("activity", ActivityPanel)
        self.register_view("metrics", CognitiveMetricsPanel)
        self.register_view("annual_evolution", AnnualEvolutionPanel)
        self.register_view("weekly_comparison", WeeklyComparisonPanel)
        self.register_view("metrics_dashboard", MetricsDashboardPanel)

        # --- INTELIGENCIA / PLANIFICACIÓN ---
        self.register_view("heuristics", HeuristicsPanel)
        self.register_view("guided_suggestions", GuidedSuggestionsPanel)
        self.register_view("guardian_plans", GuardianPlansPanel)
        self.register_view("evolution_control", EvolutionControlPanel)

        # --- MEMORIA / RAZONAMIENTO ---
        self.register_view("memory_inspector", MemoryInspectorPanel)
        self.register_view("mind_versions", MindVersionsPanel)
        self.register_view("internal_reasoning", InternalReasoningPanel)
        self.register_view("decision_replay", DecisionReplayPanel)
        self.register_view("evolution_timeline", EvolutionTimelinePanel)

        # --- PROPUESTAS / PERMISOS ---
        self.register_view("proposals", ProposalsPanel)
        self.register_view("proposal_simulator", ProposalSimulatorPanel)
        self.register_view("advanced_permissions", AdvancedPermissionsPanel)

        # --- DEPENDENCIAS / ERRORES ---
        self.register_view("cognitive_dependencies", CognitiveDependenciesPanel)
        self.register_view("dependencies_graph", CognitiveDependenciesCanvasPanel)
        self.register_view("error_patterns", ErrorPatternsPanel)
        self.register_view("error_monitor", ErrorMonitorPanel)

        # --- SOPORTE ---
        self.register_view("history", HistoryPanel)
        self.register_view("gui_hints", GuiHintsPanel)
        self.register_view("integrity", IntegrityPanel)

        # Vista inicial
        self.show_view("core")

        # ================= COMMUNICATION =================
        self.communication_panel = CommunicationPanel(self, self.memory)
        self.communication_panel.pack(
            side="bottom",
            fill="x",
            padx=6,
            pady=6
        )

    # =================================================
    # VIEW MANAGEMENT
    # =================================================
    def register_view(self, name, view_cls):
        view = view_cls(self.view_container, self.memory)
        view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.views[name] = view

    def show_view(self, name):
        if name not in self.views:
            return
        for v in self.views.values():
            v.lower()
        self.views[name].lift()

    # =================================================
    # CALLBACKS
    # =================================================
    def _on_project_selected(self, project):
        self.memory.set_active_project(project)
        self.memory.log_event(
            event="project_selected",
            summary=f"Proyecto activo: {project.get('name', '?')}"
        )