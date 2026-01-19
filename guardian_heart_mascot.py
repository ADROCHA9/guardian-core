import tkinter as tk
import os
import json
import time
import math
import subprocess
import sys

# ================= CONFIG =================
GUARDIAN_ROOT = r"C:\Users\CONECTIA BA\guardian_bot"
MEMORY_FILE = os.path.join(GUARDIAN_ROOT, "memory.json")
CONTROL_FLAG = os.path.join(GUARDIAN_ROOT, "guardian_control.flag")
BOOTSTRAP_SCRIPT = "guardian_bootstrap.py"

SIZE = 120
FPS_MS = 30
STATE_REFRESH_MS = 2000
# =========================================


class GuardianHeart(tk.Tk):
    def __init__(self):
        super().__init__()

        # ---------- ventana ----------
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="black")
        self.wm_attributes("-transparentcolor", "black")

        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()

        self.x = self.screen_w - SIZE - 20
        self.y = self.screen_h - SIZE - 60
        self.geometry(f"{SIZE}x{SIZE}+{self.x}+{self.y}")

        self.canvas = tk.Canvas(
            self, width=SIZE, height=SIZE,
            bg="black", highlightthickness=0
        )
        self.canvas.pack()

        # ---------- estado ----------
        self.learning = False
        self.cognitive_load = 0.0
        self.last_cycle = None
        self.paused = False
        self.capsule = False

        self.t = 0.0

        # ---------- corazón ----------
        self.heart = self.canvas.create_polygon(
            self._heart_points(1.0),
            fill="#ff3355",
            outline=""
        )

        # ---------- menú ----------
        self._build_menu()

        # ---------- binds ----------
        self.bind("<Button-3>", self.show_menu)

        # ---------- loops ----------
        self.after(FPS_MS, self.animate)
        self.after(STATE_REFRESH_MS, self.read_guardian_state)

    # =================================================
    # FORMA DEL CORAZÓN
    # =================================================
    def _heart_points(self, scale):
        cx, cy = SIZE // 2, SIZE // 2
        pts = []
        for a in range(0, 360, 20):
            t = math.radians(a)
            x = 16 * math.sin(t)**3
            y = (
                13 * math.cos(t)
                - 5 * math.cos(2 * t)
                - 2 * math.cos(3 * t)
                - math.cos(4 * t)
            )
            pts.append(cx + x * scale)
            pts.append(cy - y * scale)
        return pts

    # =================================================
    # ESTADO REAL DE GUARDIAN
    # =================================================
    def read_guardian_state(self):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                mem = json.load(f)

            g = mem.get("guardian_self", {})
            self.learning = g.get("learning_state") in ("learning", "passive", "cognitive")
            self.last_cycle = g.get("last_cycle")

            if self.last_cycle:
                age = time.time() - time.mktime(
                    time.strptime(self.last_cycle[:19], "%Y-%m-%dT%H:%M:%S")
                )
                self.cognitive_load = max(0.0, min(1.0, 1.0 - age / 120))
            else:
                self.cognitive_load = 0.0

        except Exception:
            pass

        self.after(STATE_REFRESH_MS, self.read_guardian_state)

    # =================================================
    # ANIMACIÓN
    # =================================================
    def animate(self):
        self.t += 0.05

        # ritmo del latido
        if self.paused:
            beat = 0.1
        elif self.learning:
            beat = 1.2
        else:
            beat = 0.6 + self.cognitive_load

        scale = 1.0 + 0.15 * math.sin(self.t * beat * 4)
        self.canvas.coords(self.heart, self._heart_points(scale))

        # color
        if self.paused:
            color = "#555555"
        else:
            r = int(180 + 75 * self.cognitive_load)
            color = f"#{r:02x}3355"

        self.canvas.itemconfig(self.heart, fill=color)

        self.after(FPS_MS, self.animate)

    # =================================================
    # MENÚ
    # =================================================
    def _build_menu(self):
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Estado Guardian", command=self.show_status)
        self.menu.add_separator()
        self.menu.add_command(label="Iniciar Guardian", command=self.start_guardian)
        self.menu.add_command(label="Pausar Guardian", command=self.pause_guardian)
        self.menu.add_command(label="Reiniciar Guardian", command=lambda: self.signal("restart"))
        self.menu.add_command(label="Apagar Guardian (limpio)", command=lambda: self.signal("shutdown"))
        self.menu.add_separator()
        self.menu.add_command(label="Modo cápsula", command=self.enter_capsule)
        self.menu.add_command(label="Salir cápsula", command=self.exit_capsule)
        self.menu.add_separator()
        self.menu.add_command(label="Cerrar mascota", command=self.destroy)

    def show_menu(self, e):
        self.menu.tk_popup(e.x_root, e.y_root)

    def show_status(self):
        self.title(
            f"Guardian | learning={self.learning} | load={self.cognitive_load:.2f}"
        )

    # =================================================
    # CONTROL GUARDIAN
    # =================================================
    def start_guardian(self):
        subprocess.Popen(
            [sys.executable, BOOTSTRAP_SCRIPT],
            cwd=GUARDIAN_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def pause_guardian(self):
        self.paused = not self.paused

    def signal(self, cmd):
        with open(CONTROL_FLAG, "w", encoding="utf-8") as f:
            f.write(cmd)

    # =================================================
    # CÁPSULA
    # =================================================
    def enter_capsule(self):
        self.capsule = True
        self.geometry(f"{SIZE//2}x{SIZE//2}+20+{self.screen_h - SIZE//2 - 20}")

    def exit_capsule(self):
        self.capsule = False
        self.geometry(f"{SIZE}x{SIZE}+{self.x}+{self.y}")


if __name__ == "__main__":
    GuardianHeart().mainloop()