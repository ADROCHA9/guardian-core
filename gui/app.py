# gui/app.py

import os
import tkinter as tk
from tkinter import messagebox

from memory import ProjectMemory
from gui.theme import THEME
from gui.layouts.main_layout import MainLayout
from gui.auth.auth_screen import AuthScreen

from security.integrity_guard import verify_integrity
from services.guardian_service_loop import start_services
from environment.environment_state import collect_environment_state
from services.live_gui_watcher import LiveGuiWatcher
from services.encoding_guard import force_utf8

force_utf8()


# =====================================================
# ROOT PATH
# =====================================================
def resolve_guardian_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# =====================================================
# APP PRINCIPAL
# =====================================================
class GuardianApp(tk.Tk):
    """
    Aplicación GUI del Guardian.

    Importante:
    - La GUI NO arranca el aprendizaje
    - Guardian ya está trabajando cuando esta app existe
    - La GUI solo observa y controla (pausa / reanudar)
    """

    def __init__(self):
        super().__init__()

        # ================= ROOT =================
        self.root_path = resolve_guardian_root()

        # ================= INTEGRITY =================
        try:
            verify_integrity(self.root_path)
        except Exception as e:
            messagebox.showerror("Integridad comprometida", str(e))
            self.destroy()
            return

        # ================= MEMORY =================
        self.memory = ProjectMemory(self.root_path)
        self.memory.load()

        # ================= ENVIRONMENT =================
        try:
            env = collect_environment_state()
            self.memory.set_environment(env)
        except Exception as e:
            self.memory.log_event(
                event="environment_detection_failed",
                summary=str(e)
            )

        # ================= START GUARDIAN (CRÍTICO) =================
        # Guardian arranca SIEMPRE, aunque la GUI no se use
        start_services(self.memory)

        # ================= WINDOW =================
        self.title("GUARDIAN")
        self.state("zoomed")
        self.configure(bg=THEME["bg"])

        # ================= FOCUS HANDLERS =================
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<FocusIn>", self._on_focus_in)

        # ================= AUTH =================
        self.auth_screen = AuthScreen(
            self,
            self.memory,
            on_success=self._on_authenticated
        )
        self.auth_screen.pack(fill="both", expand=True)

    # =====================================================
    # FOCUS CONTROL (NO DETIENE APRENDIZAJE)
    # =====================================================
    def _on_focus_out(self, _):
        self.memory.update_guardian_state({
            "mode": "background",
            "status": "idle"
        })

    def _on_focus_in(self, _):
        self.memory.update_guardian_state({
            "mode": "foreground"
        })

    # =====================================================
    # AUTH SUCCESS
    # =====================================================
    def _on_authenticated(self):
        self.auth_screen.destroy()

        # ================= MAIN LAYOUT =================
        self.main_layout = MainLayout(self, self.memory)
        self.main_layout.pack(fill="both", expand=True)

        # ================= LIVE GUI WATCHER =================
        self.gui_watcher = LiveGuiWatcher(
            root_path=self.root_path,
            on_change=self._on_gui_change
        )
        self.gui_watcher.start()

        self.memory.log_event(
            event="guardian_gui_ready",
            summary="GUI activa. Guardian continúa aprendiendo."
        )

    # =====================================================
    # LIVE GUI RELOAD
    # =====================================================
    def _on_gui_change(self, path: str):
        if not hasattr(self, "main_layout"):
            return

        path = path.lower()
        for name in list(self.main_layout.views.keys()):
            if name in path:
                self.main_layout.reload_view(name)


# =====================================================
# ENTRYPOINT
# =====================================================
def run_gui():
    """
    Ejecuta la GUI.
    Guardian ya está trabajando antes de que esto se muestre.
    """
    app = GuardianApp()
    app.mainloop()


if __name__ == "__main__":
    run_gui()