import tkinter as tk
from datetime import datetime


class LearningIndicator(tk.Frame):
    """
    Indicador visual HONESTO del aprendizaje del Guardian.

    - Muestra intensidad real
    - Cambia color según carga cognitiva
    - Refleja métricas reales
    - No decide nada
    """

    INTENSITY_COLORS = {
        "low": "#4da6ff",        # Pasivo
        "adaptive": "#5cd65c",   # Cognitivo liviano
        "focused": "#ffa500",    # Aprendizaje profundo
        "intensive": "#ff4d4d",  # Máxima intensidad permitida
        "idle": "#777777"
    }

    def __init__(self, parent, memory=None):
        super().__init__(parent, bg="#1e1e1e")
        self.memory = memory

        self._pulse = False
        self._base_color = self.INTENSITY_COLORS["idle"]

        # Línea principal
        self.label = tk.Label(
            self,
            text="● Guardian idle",
            fg=self._base_color,
            bg="#1e1e1e",
            font=("Consolas", 9)
        )
        self.label.pack(anchor="w", padx=6, pady=(2, 0))

        # Detalle
        self.details = tk.Label(
            self,
            text="",
            fg="#aaaaaa",
            bg="#1e1e1e",
            font=("Consolas", 8)
        )
        self.details.pack(anchor="w", padx=8, pady=(0, 2))

    # =================================================
    # ACTUALIZACIÓN DESDE MEMORIA (FUENTE REAL)
    # =================================================
    def refresh(self):
        if not self.memory:
            return

        guardian = self.memory.get("guardian_self", {})
        window = guardian.get("learning_window")

        if not window:
            self.set_idle()
            return

        intensity = window.get("intensity", "adaptive")
        learning_type = window.get("type", "cognitive")

        self.set_learning(intensity, learning_type)

    # =================================================
    # ESTADOS
    # =================================================
    def set_idle(self):
        self._pulse = False
        self._base_color = self.INTENSITY_COLORS["idle"]
        self.label.config(text="● Guardian idle", fg=self._base_color)
        self.details.config(text="")

    def set_learning(self, intensity: str, learning_type: str):
        self._pulse = True

        color = self.INTENSITY_COLORS.get(intensity, "#ffffff")
        self._base_color = color

        label = f"● Guardian aprendiendo ({learning_type})"
        self.label.config(text=label, fg=color)

        # Métricas reales
        detail = self._build_metrics_text()
        self.details.config(text=detail)

        self._animate()

    # =================================================
    # MÉTRICAS REALES
    # =================================================
    def _build_metrics_text(self) -> str:
        cognitive = self.memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {})
        daily = metrics.get("daily", {})

        today = datetime.utcnow().date().isoformat()
        today_data = daily.get(today)

        if not today_data:
            return "Sin métricas aún"

        return (
            f"Usados: {today_data.get('concepts_used', 0)} | "
            f"Dominados: {today_data.get('concepts_dominated', 0)} | "
            f"Frágiles: {today_data.get('fragile', 0)}"
        )

    # =================================================
    # ANIMACIÓN SUAVE (TITILO)
    # =================================================
    def _animate(self):
        if not self._pulse:
            return

        current = self.label.cget("fg")
        next_color = "#ffffff" if current == self._base_color else self._base_color
        self.label.config(fg=next_color)

        self.after(600, self._animate)