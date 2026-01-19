import tkinter as tk
from tkinter import messagebox
import threading
import time

from gui.theme import THEME
from services.communication_bridge import CommunicationBridge
from services.integration_manager import IntegrationManager
from gui.widgets.learning_indicator import LearningIndicator


class CommunicationPanel(tk.Frame):
    """
    Panel de comunicación viva Humano ↔ Guardian.
    NO bloquea la GUI.
    El indicador refleja APRENDIZAJE REAL, no estados simulados.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory

        # Bridge (cerebro en background)
        self.bridge = CommunicationBridge(
            memory,
            self._on_guardian_response
        )

        # UI
        self._build()

        # Indicador de aprendizaje (solo visual)
        self.learning_indicator = LearningIndicator(self, memory)
        self.learning_indicator.pack(anchor="w", padx=10, pady=2)

        # Heartbeat visual (no bloqueante)
        self.after(1500, self._learning_heartbeat)

    # =================================================
    # HEARTBEAT DE APRENDIZAJE (LECTURA DE ESTADO REAL)
    # =================================================
    def _learning_heartbeat(self):
        """
        Refleja el estado REAL del aprendizaje del Guardian.
        No decide nada. Solo observa memoria.
        """
        try:
            # El indicador ya sabe leer memoria e intensidad
            self.learning_indicator.refresh()
        except Exception:
            # Nunca romper la GUI
            self.learning_indicator.set_idle()

        # Repetir pulso
        self.after(1500, self._learning_heartbeat)

    # =================================================
    # UI
    # =================================================
    def _build(self):
        header = tk.Label(
            self,
            text="💬 Comunicación con Guardian",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        header.pack(anchor="w", padx=10, pady=4)

        self.input = tk.Text(
            self,
            height=4,
            bg=THEME["bg"],
            fg=THEME["text_main"],
            insertbackground=THEME["accent"],
            wrap="word"
        )
        self.input.pack(fill="x", padx=10, pady=4)

        btn_frame = tk.Frame(self, bg=THEME["panel_bg"])
        btn_frame.pack(fill="x", padx=10, pady=4)

        tk.Button(
            btn_frame,
            text="Enviar a Guardian",
            command=self._send
        ).pack(side="right")

        tk.Button(
            btn_frame,
            text="Integrar cambios aprobados",
            fg="white",
            bg=THEME.get("accent", "#2c7be5"),
            command=self._integrate_changes
        ).pack(side="left")

        self.output = tk.Text(
            self,
            height=12,
            bg=THEME["bg"],
            fg=THEME["text_dim"],
            state="disabled",
            wrap="word"
        )
        self.output.pack(fill="x", padx=10, pady=4)

    # =================================================
    # ACCIONES
    # =================================================
    def _send(self):
        text = self.input.get("1.0", "end").strip()
        if not text:
            return

        self.input.delete("1.0", "end")
        self._append_output(f"🧑‍💻 Vos:\n{text}\n")

        threading.Thread(
            target=self.bridge.receive,
            args=(text,),
            daemon=True
        ).start()

    def _integrate_changes(self):
        confirm = messagebox.askyesno(
            "Confirmar integración",
            "¿Querés integrar los cambios aprobados?\n\n"
            "Los cambios serán reversibles."
        )
        if not confirm:
            return

        manager = IntegrationManager(self.memory)
        result = manager.apply_approved()
        self._append_output(f"🔧 Integración:\n{result}\n")

    # =================================================
    # RESPUESTA DEL GUARDIAN
    # =================================================
    def _on_guardian_response(self, text: str):
        self._append_output(f"🛡 Guardian:\n{text}\n")

    def _append_output(self, text: str):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.config(state="disabled")