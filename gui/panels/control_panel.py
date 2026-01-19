import tkinter as tk


class ControlPanel(tk.Frame):
    """
    Control suave del aprendizaje.
    """

    def __init__(self, parent, memory):
        super().__init__(parent)
        self.memory = memory

        tk.Button(self, text="⏸ Pausar aprendizaje", command=self.pause).pack(side="left", padx=5)
        tk.Button(self, text="▶ Reanudar aprendizaje", command=self.resume).pack(side="left", padx=5)

    def pause(self):
        self.memory._memory.setdefault("guardian_self", {})["paused"] = True
        self.memory._persist()

    def resume(self):
        self.memory._memory.setdefault("guardian_self", {})["paused"] = False
        self.memory._persist()