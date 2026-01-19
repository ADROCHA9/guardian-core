from typing import Dict, List
import uuid


def generate_proposals(memory_snapshot: Dict) -> List[Dict]:
    proposals = []

    files = memory_snapshot.get("files", {})
    relations = memory_snapshot.get("relations", [])
    inconsistencies = memory_snapshot.get("inconsistencies", [])
    existing_proposals = memory_snapshot.get("proposed_connections", [])

    already_proposed = {
        (p.get("from"), p.get("to"), p.get("type"))
        for p in existing_proposals
    }

    # 1️⃣ Propuestas por módulos aislados
    for issue in inconsistencies:
        if issue.get("type") == "functional_isolation":
            file_path = issue.get("file")

            proposal_key = (file_path, "core", "integration")
            if proposal_key in already_proposed:
                continue

            proposals.append({
                "id": f"P-{uuid.uuid4().hex[:8]}",
                "type": "integration",
                "from": file_path,
                "to": "núcleo",
                "priority": "alta",
                "description": (
                    f"El módulo '{file_path}' está bien implementado pero aislado. "
                    "Se propone integrarlo al núcleo para reforzar coherencia."
                ),
                "benefit": "mejora trazabilidad y cohesión sistémica",
                "risk": "bajo",
                "status": "propuesta"
            })

    # 2️⃣ Propuestas por duplicación de rol
    role_map = {}
    for path, data in files.items():
        role = data.get("role")
        if role:
            role_map.setdefault(role, []).append(path)

    for role, paths in role_map.items():
        if len(paths) > 1:
            proposals.append({
                "id": f"P-{uuid.uuid4().hex[:8]}",
                "type": "consolidation",
                "from": paths,
                "to": role,
                "priority": "media",
                "description": (
                    f"Se detectaron múltiples módulos con el rol '{role}'. "
                    "Se propone evaluar consolidación o coordinación explícita."
                ),
                "benefit": "reduce duplicación y complejidad",
                "risk": "medio",
                "status": "propuesta"
            })

    # 3️⃣ Propuestas por núcleo débil
    central_modules = [
        r for r in relations if r.get("type") == "central_module"
    ]

    if not central_modules:
        proposals.append({
            "id": f"P-{uuid.uuid4().hex[:8]}",
            "type": "architecture",
            "from": "sistema",
            "to": "núcleo",
            "priority": "alta",
            "description": (
                "No se detecta un núcleo claramente dominante. "
                "Se propone reforzar un módulo central de orquestación."
            ),
            "benefit": "mejora gobernanza del sistema",
            "risk": "medio",
            "status": "propuesta"
        })

    return proposals