from typing import Dict, List
import uuid


def generate_questions(memory_snapshot: Dict) -> List[Dict]:
    questions = []

    files = memory_snapshot.get("files", {})
    inconsistencies = memory_snapshot.get("inconsistencies", [])
    open_questions = memory_snapshot.get("open_questions", [])

    already_asked_contexts = {
        q.get("context") for q in open_questions
    }

    # 1️⃣ Intención no confirmada
    for path, data in files.items():
        intent = data.get("intent", {}).get("why_it_exists", "")
        if "pendiente" in intent.lower() and path not in already_asked_contexts:
            questions.append({
                "id": f"Q-{uuid.uuid4().hex[:8]}",
                "context": path,
                "type": "intent_clarification",
                "question": (
                    f"¿Cuál es el propósito real del módulo '{path}' "
                    "dentro del sistema?"
                ),
                "options": [
                    "núcleo",
                    "soporte",
                    "experimental",
                    "temporal",
                    "otro"
                ],
                "status": "pending"
            })

    # 2️⃣ Inconsistencias conceptuales
    for issue in inconsistencies:
        if issue.get("type") in (
            "conceptual_drift",
            "new_module_uncontextualized"
        ):
            context = issue.get("file")
            if context and context not in already_asked_contexts:
                questions.append({
                    "id": f"Q-{uuid.uuid4().hex[:8]}",
                    "context": context,
                    "type": "conceptual_alignment",
                    "question": (
                        f"Se detectó una posible desalineación en '{context}'. "
                        "¿Debe integrarse al propósito principal o mantenerse aislado?"
                    ),
                    "options": [
                        "integrar al núcleo",
                        "mantener aislado",
                        "eliminar",
                        "definir más adelante"
                    ],
                    "status": "pending"
                })

    return questions