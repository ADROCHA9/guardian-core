# guardian_launcher.py
from memory import ProjectMemory
from services.service_loop import ServiceLoop
from gui.app import run_gui

ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"

memory = ProjectMemory(ROOT)
memory.load()

services = ServiceLoop(memory)
services.start()

run_gui(memory)