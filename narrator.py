from typing import Dict, List


def narrate_system(memory_snapshot: Dict) -> Dict[str, str]:
    project = memory_snapshot.get("project", {})
    files = memory_snapshot.get("files", {})
    relations = memory_snapshot.get("relations", [])
    inconsistencies = memory_snapshot.get("inconsistencies", [])
    evolution_log = memory_snapshot.get("evolution_log", [])

    narration = {}

    # 1️⃣ Identidad del sistema
    narration["identity"] = (
        f"{project.get('name', 'El sistema')} es un proyecto cuyo propósito es "
        f"'{project.get('purpose', 'no definido')}'. "
        f"Actualmente contiene {len(files)} módulos analizados."
    )

    # 2️⃣ Núcleo y estructura
    core_modules = [
        path for path, data in files.items()
        if "núcleo" in data.get("role", "").lower()
    ]

    narration["structure"] = (
        f"El sistema posee {len(core_modules)} módulos considerados núcleo. "
        f"Estos módulos concentran la orquestación y la lógica central."
        if core_modules else
        "No se detecta un núcleo claramente definido."
    )

    # 3️⃣ Relaciones y conectividad
    orphan_modules = [
        r.get("file") for r in relations
        if r.get("type") == "orphan_module"
    ]

    narration["connectivity"] = (
        f"Se detectaron {len(orphan_modules)} módulos aislados que no están "
        f"integrados plenamente al sistema."
        if orphan_modules else
        "La mayoría de los módulos presentan algún grado de integración."
    )

    # 4️⃣ Riesgos e inconsistencias
    high_issues = [
        i for i in inconsistencies
        if i.get("level") == "high"
    ]

    narration["risks"] = (
        f"Existen {len(high_issues)} inconsistencias de severidad alta que "
        f"requieren atención prioritaria."
        if high_issues else
        "No se detectan riesgos críticos inmediatos."
    )

    # 5️⃣ Evolución reciente
    recent_events = evolution_log[-5:]

    if recent_events:
        narration["evolution"] = (
            "La evolución reciente del sistema muestra los siguientes eventos: "
            + "; ".join(e.get("event") for e in recent_events)
        )
    else:
        narration["evolution"] = "No hay historial evolutivo registrado aún."

    # 6️⃣ Evaluación global
    narration["summary"] = (
        "El sistema se encuentra en un estado de observación consciente, "
        "con estructura definida pero aún en proceso de consolidación."
    )

    return narration