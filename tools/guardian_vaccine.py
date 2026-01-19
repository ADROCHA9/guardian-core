# tools/guardian_vaccine.py
import json
import platform
import uuid
from datetime import datetime

def probe_hardware() -> dict:
    try:
        import psutil
        cpu = {
            "cores_logical": psutil.cpu_count(logical=True),
            "cores_physical": psutil.cpu_count(logical=False),
            "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
            "usage_percent": psutil.cpu_percent(interval=0.5),
        }
        mem = psutil.virtual_memory()._asdict()
    except Exception:
        cpu, mem = {}, {}

    return {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu": cpu,
        "memory": mem,
    }

def main():
    node_profile = {
        "node_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
        },
        "hardware": probe_hardware(),
        "consent": {
            "type": "manual_execution",
            "operator": "Adrian",
            "scope": "diagnostic_only"
        }
    }

    out = {
        "node_profile": node_profile,
        "instructions": (
            "Este archivo fue generado por ejecución manual.\n"
            "Copiar 'node_profile.json' al Guardian central para registro.\n"
            "No se ejecutó ninguna acción sobre el sistema."
        )
    }

    with open("node_profile.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("✔ Vacuna ejecutada manualmente.")
    print("✔ Perfil generado: node_profile.json")
    print("✔ Ninguna acción fue ejecutada sobre el sistema.")

if __name__ == "__main__":
    main()