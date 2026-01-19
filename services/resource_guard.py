import psutil

MAX_RAM_PERCENT = 40

def enforce_resource_limits(memory):
    ram = psutil.virtual_memory().percent

    if ram > MAX_RAM_PERCENT:
        memory.log_event(
            event="resource_limit_reached",
            summary=f"RAM {ram}% — limpieza preventiva activada"
        )

        # marcar limpieza agresiva
        memory._memory["services"]["cleanup_mode"] = "aggressive"