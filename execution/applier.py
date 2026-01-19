# execution/applier.py
import os
from datetime import datetime
from typing import Dict, List


def apply_changes(
    memory,
    changes: List[Dict],
    require_identity: bool = True
) -> None:
    """
    Aplica cambios reales al proyecto.
    Solo debe llamarse tras confirmación humana explícita.
    """

    # =====================================================
    # Verificación de identidad
    # =====================================================
    if require_identity:
        identity = memory.get("identity") or {}
        if not identity.get("last_verified") and not identity.get("born_at"):
            raise RuntimeError(
                "Identidad no verificada. No se pueden aplicar cambios."
            )

    root = memory.get("project", {}).get("root_path")
    if not root:
        raise RuntimeError("Ruta raíz del proyecto desconocida")

    applied = []

    for change in changes:
        file_path = change.get("file")
        content = change.get("content")

        if not file_path or content is None:
            continue

        full_path = os.path.join(root, file_path)

        # Crear carpetas si no existen
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Escribir archivo
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        applied.append(file_path)

    # =====================================================
    # Registro de evolución
    # =====================================================
    memory._memory.setdefault("evolution_log", [])
    memory._memory["evolution_log"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "changes_applied",
        "files": applied
    })

    # Actualizar estado del Guardian
    memory._memory.setdefault("guardian_self", {})
    memory._memory["guardian_self"]["status"] = "evolved"

    memory._persist()