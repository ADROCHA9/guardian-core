# gui/auth/auth_screen.py
import tkinter as tk
from tkinter import messagebox

from gui.theme import THEME
from security.voice.audio_capture import capture_voice
from security.identity_manager import (
    is_operator_registered,
    register_operator,
    authenticate_operator
)


class AuthScreen(tk.Frame):
    """
    Registro inicial del operador + autenticación posterior.
    """

    def __init__(self, parent, memory, on_success):
        super().__init__(parent, bg=THEME["bg"])
        self.memory = memory
        self.on_success = on_success
        self._build()

    def _build(self):
        self.registered = is_operator_registered(self.memory)

        title = "Registro del Operador" if not self.registered else "Autenticación"
        tk.Label(
            self,
            text=title,
            fg=THEME["accent"],
            bg=THEME["bg"],
            font=THEME["font_title"]
        ).pack(pady=20)

        if not self.registered:
            tk.Label(self, text="Nombre del operador").pack()
            self.operator = tk.Entry(self)
            self.operator.pack(pady=4)

        tk.Label(self, text="Contraseña").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=4)

        self.info = tk.Label(
            self,
            text="",
            fg=THEME["text_dim"],
            bg=THEME["bg"]
        )
        self.info.pack(pady=6)

        tk.Button(
            self,
            text="Continuar",
            command=self._process
        ).pack(pady=20)

    def _process(self):
        pwd = self.password.get().strip()
        if not pwd:
            messagebox.showerror("Error", "Contraseña requerida")
            return

        try:
            if not self.registered:
                name = self.operator.get().strip()
                if not name:
                    messagebox.showerror("Error", "Nombre requerido")
                    return

                messagebox.showinfo(
                    "Registro de voz",
                    "A continuación se grabará tu voz para registrar identidad.\n"
                    "Hablá con normalidad durante 3 segundos."
                )

                audio = capture_voice(duration=3.0)

                register_operator(
                    self.memory,
                    operator=name,
                    password=pwd,
                    audio_bytes=audio
                )

                messagebox.showinfo(
                    "Registro completo",
                    "Operador registrado correctamente.\n"
                    "Reiniciá Guardian para autenticar."
                )
                self.master.destroy()

            else:
                messagebox.showinfo(
                    "Autenticación de voz",
                    "A continuación se grabará tu voz para autenticar.\n"
                    "Hablá con normalidad durante 3 segundos."
                )

                audio = capture_voice(duration=3.0)

                ok = authenticate_operator(
                    self.memory,
                    password=pwd,
                    audio_bytes=audio
                )

                if not ok:
                    raise RuntimeError("Credenciales inválidas")

                self.on_success()

        except Exception as e:
            messagebox.showerror("Error", str(e))