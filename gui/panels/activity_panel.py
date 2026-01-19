import tkinter as tk


class ActivityPanel(tk.Frame):
    """
    Actividad cognitiva reciente del Guardian.
    """

    def __init__(self, parent, memory):
        super().__init__(parent)
        self.memory = memory

        self.text = tk.Text(self, height=14, state="disabled", wrap="word")
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        self.after(2000, self.refresh)

    def refresh(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        log = self.memory.get("evolution_log", [])[-15:]
        for e in log:
            self.text.insert("end", f"{e.get('event')}: {e.get('summary')}\n")

        self.text.config(state="disabled")
        self.after(2000, self.refresh)