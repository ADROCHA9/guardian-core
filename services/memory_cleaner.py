# services/memory_cleaner.py
import psutil
from datetime import datetime, timedelta

MAX_RAM_PERCENT = 40
MAX_LOG_EVENTS = 500
MAX_PROPOSALS = 100
MAX_INCONSISTENCIES = 100

def clean_memory(memory):
    ram = psutil.virtual_memory().percent
    if ram < MAX_RAM_PERCENT:
        return

    # Limpiar logs antiguos
    logs = memory.get("evolution_log", [])
    if len(logs) > MAX_LOG_EVENTS:
        memory._memory["evolution_log"] = logs[-MAX_LOG_EVENTS:]

    # Limpiar propuestas antiguas
    proposals = memory.get("proposed_connections", [])
    if len(proposals) > MAX_PROPOSALS:
        memory._memory["proposed_connections"] = proposals[-MAX_PROPOSALS:]

    # Limpiar inconsistencias antiguas
    inc = memory.get("inconsistencies", [])
    if len(inc) > MAX_INCONSISTENCIES:
        memory._memory["inconsistencies"] = inc[-MAX_INCONSISTENCIES:]

    memory.log_event(
        event="memory_cleaned",
        summary=f"Limpieza automática ejecutada (RAM {ram}%)"
    )