import json
import os
from datetime import datetime


class MentalStateImportTask:
    """
    Importa y restaura un estado mental exportado de Guardian.

    Reglas:
    - No ejecuta código
    - No modifica el filesystem
    - Solo restaura memoria cognitiva
    - Debe ser llamado bajo permiso humano
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self, file_path: str) -> dict:
        if not file_path:
            raise ValueError("Ruta de archivo no especificada")

        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError("Archivo JSON inválido") from e

        # -------------------------------
        # Validación mínima de estructura
        # -------------------------------
        if not isinstance(data, dict):
            raise ValueError("El estado mental debe ser un objeto JSON")

        if "guardian_self" not in data:
            raise ValueError("Estado mental inválido: falta guardian_self")

        if "cognitive_memory" not in data:
            raise ValueError("Estado mental inválido: falta cognitive_memory")

        # -------------------------------
        # Backup previo (seguridad)
        # -------------------------------
        backup = {
            "backup_at": datetime.utcnow().isoformat(),
            "guardian_self": self.memory._memory.get("guardian_self"),
            "cognitive_memory": self.memory._memory.get("cognitive_memory"),
        }

        self.memory._memory.setdefault("backups", []).append(backup)

        # -------------------------------
        # Restauración
        # -------------------------------
        self.memory._memory["guardian_self"] = data["guardian_self"]
        self.memory._memory["cognitive_memory"] = data["cognitive_memory"]

        self.memory.log_event(
            event="mental_state_imported",
            summary=f"Estado mental importado desde {os.path.basename(file_path)}"
        )

        self.memory._persist()

        return {
            "status": "imported",
            "imported_at": datetime.utcnow().isoformat(),
            "source": file_path
        }