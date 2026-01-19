# services/auto_proposal_engine.py

def generate_auto_proposals(memory):
    files = memory.get("files") or {}
    relations = memory.get("relations") or []
    inconsistencies = memory.get("inconsistencies") or []

    proposals = []

    # Heurística 1: archivos aislados
    related_files = {r["source"] for r in relations} | {r["target"] for r in relations}

    for path, data in files.items():
        if path not in related_files:
            proposals.append({
                "title": "Archivo aislado detectado",
                "description": f"{path} no está conectado al sistema.",
                "priority": "medium",
                "origin": "auto_proposal",
                "action": "suggest_integration"
            })

    # Heurística 2: inconsistencias acumuladas
    if len(inconsistencies) >= 3:
        proposals.append({
            "title": "Inconsistencias recurrentes",
            "description": "Se detectaron múltiples inconsistencias. Posible deuda técnica.",
            "priority": "high",
            "origin": "auto_proposal",
            "action": "suggest_refactor"
        })

    return proposals