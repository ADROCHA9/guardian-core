import tkinter as tk
from gui.theme import THEME
from gui.animation_engine import AnimationEngine

from gui.widgets.guardian_pulse import GuardianPulse
from gui.widgets.project_pulse import ProjectPulse
from gui.widgets.guardian_dna import GuardianDNA
from gui.widgets.project_dna import ProjectDNA

from gui.panels.environment_panel import EnvironmentPanel
from gui.panels.nodes_panel import NodesPanel
from gui.panels.security_panel import SecurityPanel
from gui.panels.evolution_panel import EvolutionPanel


class CoreView(tk.Frame):
    """
    Núcleo Operativo Visual del Guardian.
    Solo refleja estado real desde memory.
    """

    def __init__(self, parent, memory, anim_engine=None):
        super().__init__(parent, bg=THEME["bg"])
        self.memory = memory
        self.anim = anim_engine or AnimationEngine(self)

        self._build_static()
        self._build_dynamic()

        self.anim.start()

    # =====================================================
    # UI ESTÁTICA
    # =====================================================
    def _build_static(self):
        tk.Label(
            self,
            text="GUARDIAN — Núcleo Operativo",
            bg=THEME["bg"],
            fg=THEME["accent"],
            font=THEME["font_title"]
        ).pack(pady=20)

        self.status_label = tk.Label(
            self,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            font=THEME["font_main"],
            justify="left"
        )
        self.status_label.pack(pady=10)

        pulses = tk.Frame(self, bg=THEME["bg"])
        pulses.pack(pady=10)

        self.guardian_pulse = GuardianPulse(pulses, self.memory)
        self.guardian_pulse.pack(pady=4)

        self.project_pulse = ProjectPulse(pulses, self.memory)
        self.project_pulse.pack(pady=4)

        self.guardian_dna = GuardianDNA(self, self.memory)
        self.guardian_dna.pack(pady=6)

        self.project_dna = ProjectDNA(self, self.memory)
        self.project_dna.pack(pady=6)

        panels = tk.Frame(self, bg=THEME["bg"])
        panels.pack(fill="x", pady=10)

        self.environment_panel = EnvironmentPanel(panels, self.memory)
        self.environment_panel.pack(side="left", expand=True, fill="both", padx=4)

        self.nodes_panel = NodesPanel(panels, self.memory)
        self.nodes_panel.pack(side="left", expand=True, fill="both", padx=4)

        self.security_panel = SecurityPanel(panels, self.memory)
        self.security_panel.pack(side="left", expand=True, fill="both", padx=4)

        self.evolution_panel = EvolutionPanel(panels, self.memory)
        self.evolution_panel.pack(side="left", expand=True, fill="both", padx=4)

    # =====================================================
    # UI DINÁMICA (ANIMACIÓN GLOBAL ÚNICA)
    # =====================================================
    def _build_dynamic(self):
        for component in [
            self.guardian_pulse,
            self.project_pulse,
            self.guardian_dna,
            self.project_dna,
            self.environment_panel,
            self.nodes_panel,
            self.security_panel,
            self.evolution_panel,
        ]:
            self.anim.add(component.update)

        self.anim.add(self._update_status)

    def _update_status(self, dt):
        env = self.memory.get("environment", {})
        guardian = self.memory.get("guardian_self", {})

        self.status_label.config(
            text=(
                f"Modo: {env.get('mode', {}).get('mode', 'UNKNOWN')}\n"
                f"Nivel Evolutivo: {guardian.get('evolution_level', 0)}\n"
                f"Estado: {guardian.get('status', 'stable')}\n"
                f"Propuestas: {len(self.memory.get('proposed_connections', []))}"
            )
        )