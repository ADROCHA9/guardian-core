# execution/applier.py
import os
import shutil
from datetime import datetime
from typing import Dict, List


class ApplyError(Exception):
    pass


def apply_changes(
    *,
    sandbox_path: str,
    project_root: str,
    changes: List[Dict],
    memory
) -> Dict[str, any]:
    """
    Aplica cambios reales al proyecto desde una sandbox validada.

    changes = [
        {
            "file": "ruta/relativa.py",
            "sandbox_path": "/tmp/sandbox/.../archivo.py"
        }
    ]
    """

    applied = []
    timestamp = datetime.utcnow().isoformat()

    for change in changes:
        rel_path = change["file"]
        src = change["sandbox_path"]
        dst = os.path.join(project_root, rel_path)

        if not os.path.exists(src):
            raise ApplyError(f"No existe el archivo sandbox: {src}")

        # Backup automático
        backup_path = dst + f".backup_{timestamp}"
        if os.path.exists(dst):
            shutil.copy2(dst, backup_path)

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

        applied.append({
            "file": rel_path,
            "backup": backup_path if os.path.exists(backup_path) else None
        })

    # Registrar en memoria
    memory.log_event(
        event="changes_applied",
        summary=f"{len(applied)} archivos actualizados"
    )

    memory._memory.setdefault("applied_changes", []).append({
        "timestamp": timestamp,
        "changes": applied
    })

    memory._persist()

    return {
        "status": "applied",
        "files": applied,
        "timestamp": timestamp
    }