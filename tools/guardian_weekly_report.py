#!/usr/bin/env python3

import json
import os
from datetime import datetime
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KNOWLEDGE_FILE = os.path.join(BASE_DIR, ".project_knowledge.json")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "weekly")

os.makedirs(REPORT_DIR, exist_ok=True)

now = datetime.utcnow()
date_str = now.strftime("%Y-%m-%d")
report_path = os.path.join(REPORT_DIR, f"guardian_report_{date_str}.txt")

with open(KNOWLEDGE_FILE, "r") as f:
    data = json.load(f)

guardian = data.get("guardian_self", {})
memory = data.get("cognitive_memory", {})
evolution_log = data.get("evolution_log", [])

report_lines = []

def line(txt=""):
    report_lines.append(txt)

# ======================================================
# ENCABEZADO
# ======================================================
line("GUARDIAN – REPORTE SEMANAL DE EVOLUCIÓN")
line("=" * 50)
line(f"Fecha UTC: {now.isoformat()}")
line()

# ======================================================
# ESTADO GENERAL
# ======================================================
line("ESTADO GENERAL")
line("-" * 20)
line(f"Estado: {guardian.get('status')}")
line(f"Modo cognitivo: {guardian.get('mode')}")
line(f"Memory mode: {guardian.get('memory_mode')}")
line(f"Learning mode: {guardian.get('learning_mode')}")
line(f"Heartbeat actual: {guardian.get('heartbeat')}")
line()

# ======================================================
# APRENDIZAJE Y MEMORIA
# ======================================================
line("APRENDIZAJE Y MEMORIA")
line("-" * 20)
line(f"Decisiones registradas: {len(memory.get('decisions', []))}")
line(f"Ideas crudas activas: {len(memory.get('raw_ideas', []))}")
line(f"Patrones detectados: {len(memory.get('patterns', []))}")
line(f"Entradas de Python aprendidas: {len(memory.get('python_knowledge', []))}")
line()

# ======================================================
# EVOLUCIÓN
# ======================================================
line("EVOLUCIÓN RECIENTE")
line("-" * 20)
recent_events = evolution_log[-10:]
if recent_events:
    for ev in recent_events:
        line(f"- {ev.get('timestamp')} :: {ev.get('event')} :: {ev.get('summary', '')}")
else:
    line("Sin eventos recientes.")
line()

# ======================================================
# AUTO-EVALUACIÓN (DERIVADA)
# ======================================================
line("AUTO-EVALUACIÓN")
line("-" * 20)

if guardian.get("learning_mode") == "aggressive":
    line("✔ Aprendizaje agresivo activo.")
else:
    line("⚠ Aprendizaje no agresivo.")

if guardian.get("memory_mode") == "growth":
    line("✔ Memoria en modo crecimiento.")
else:
    line("⚠ Memoria no está en growth.")

line("Guardian continúa operando de forma autónoma y estable.")
line()

# ======================================================
# PROPUESTAS DE EVOLUCIÓN (NO EJECUTADAS)
# ======================================================
line("PROPUESTAS DE EVOLUCIÓN")
line("-" * 20)
line("- Incrementar correlación entre errores y aprendizaje Python.")
line("- Expandir generación de hipótesis internas.")
line("- Introducir resúmenes mensuales de conocimiento.")
line()

# ======================================================
# CIERRE
# ======================================================
line("FIN DEL REPORTE")
line("=" * 50)

with open(report_path, "w") as f:
    f.write("\n".join(report_lines))

# ======================================================
# GIT COMMIT + PUSH
# ======================================================
try:
    subprocess.run(["git", "add", report_path], cwd=BASE_DIR, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"Guardian weekly report {date_str}"],
        cwd=BASE_DIR,
        check=True,
    )
    subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
except Exception as e:
    print("Git push failed:", e)
