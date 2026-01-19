from typing import Dict, List


def evaluate_user_idea(idea: str, memory_snapshot: Dict) -> Dict[str, any]:
    idea_l = idea.lower()

    files = memory_snapshot.get("files", {})
    relations = memory_snapshot.get("relations", [])
    proposals = memory_snapshot.get("proposed_connections", [])
    inconsistencies = memory_snapshot.get("inconsistencies", [])
    project = memory_snapshot.get("project", {})

    result = {
        "idea": idea,
        "status": "no evaluada",
        "summary": "",
        "alignment": "desconocida",
        "already_exists": False,
        "similar_proposal": None,
        "affected_modules": [],
        "recommendation": "",
        "risks": [],
        "next_steps": []
    }

    # 1️⃣ ¿La idea ya existe?
    for path, data in files.items():
        role = data.get("role", "").lower()
        intent = data.get("intent", {}).get("what_it_does", "").lower()

        if idea_l in role or idea_l in intent:
            result["already_exists"] = True
            result["status"] = "ya implementada"
            result["summary"] = (
                f"La idea parece ya estar cubierta por el módulo '{path}'."
            )
            result["affected_modules"].append(path)
            result["recommendation"] = (
                "Revisar y reforzar el módulo existente antes de crear uno nuevo."
            )
            return result

    # 2️⃣ ¿El sistema ya propuso algo similar?
    for p in proposals:
        desc = p.get("description", "").lower()
        if any(word in desc for word in idea_l.split()):
            result["similar_proposal"] = p["description"]
            result["status"] = "alineada con propuesta del sistema"

    # 3️⃣ Alineación con el propósito
    purpose = project.get("purpose", "").lower()
    if purpose and any(word in idea_l for word in purpose.split()):
        result["alignment"] = "alta"
    else:
        result["alignment"] = "media"

    # 4️⃣ Impacto potencial
    for r in relations:
        if r.get("type") in ("central_module", "dependency"):
            result["affected_modules"].append(r.get("file") or r.get("to"))

    result["affected_modules"] = list(set(result["affected_modules"]))

    # 5️⃣ Riesgos actuales
    if inconsistencies:
        result["risks"].append(
            "Existen inconsistencias activas que podrían amplificarse."
        )

    # 6️⃣ Recomendación final
    result["status"] = result["status"] if result["status"] != "no evaluada" else "viable con condiciones"
    result["summary"] = (
        "La idea es conceptualmente válida, pero requiere integración consciente."
    )
    result["recommendation"] = (
        "Definir claramente su rol, puntos de integración y relación con el núcleo."
    )
    result["next_steps"] = [
        "confirmar propósito exacto",
        "evaluar impacto en módulos centrales",
        "decidir prioridad frente a propuestas existentes"
    ]

    return result