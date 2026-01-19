import copy
from datetime import datetime


class IntegrationManager:
    """
    Aplica y revierte evoluciones aprobadas
    de forma controlada y auditable.
    """

    def __init__(self, memory):
        self.memory = memory

    # =================================================
    # INTEGRACIÓN
    # =================================================
    def apply_approved(self) -> str:
        proposals = self.memory.get("proposed_connections") or []
        approved = [p for p in proposals if p.get("status") == "approved"]

        if not approved:
            return "⚠️ No hay propuestas aprobadas para integrar."

        backup = self._create_backup()

        applied = []
        for proposal in approved:
            try:
                self._apply_proposal(proposal)
                proposal["status"] = "integrated"
                proposal["integrated_at"] = datetime.utcnow().isoformat()
                applied.append(proposal)
            except Exception as e:
                self._restore_backup(backup)
                self.memory.log_event(
                    event="integration_failed",
                    summary=str(e)
                )
                self.memory._persist()
                return "❌ Falló la integración. Se restauró el estado previo."

        self.memory.log_event(
            event="integration_completed",
            summary=f"{len(applied)} propuestas integradas"
        )

        self.memory._persist()
        return "✅ Integración completada correctamente."

    # =================================================
    # ROLLBACK
    # =================================================
    def rollback_to(self, index: int) -> str:
        backups = self.memory.get("backups") or []

        if not backups:
            return "⚠️ No hay backups disponibles."

        if index < 0 or index >= len(backups):
            return "❌ Índice de backup inválido."

        snapshot = backups[index]["snapshot"]

        self.memory._memory.clear()
        self.memory._memory.update(copy.deepcopy(snapshot))

        self.memory.log_event(
            event="rollback_executed",
            summary=f"Rollback al backup #{index}"
        )

        self.memory._persist()
        return f"🔁 Rollback aplicado al estado #{index}."

    # =================================================
    # APLICACIÓN INTERNA
    # =================================================
    def _apply_proposal(self, proposal: dict):
        p_type = proposal.get("type")

        if p_type == "new_module":
            files = self.memory._memory.setdefault("files", {})
            files[proposal["id"]] = {
                "description": proposal.get("description"),
                "created_at": datetime.utcnow().isoformat()
            }

        elif p_type == "refactor":
            relations = self.memory._memory.setdefault("relations", [])
            relations.append({
                "refactor": proposal.get("description"),
                "timestamp": datetime.utcnow().isoformat()
            })

        elif p_type == "cleanup":
            inconsistencies = self.memory._memory.get("inconsistencies", [])
            if inconsistencies:
                inconsistencies.pop()

        else:
            raise ValueError(f"Tipo de propuesta desconocido: {p_type}")

        self.memory.log_event(
            event="proposal_applied",
            summary=f"Propuesta {proposal.get('id')} aplicada"
        )

    # =================================================
    # BACKUP
    # =================================================
    def _create_backup(self) -> dict:
        snapshot = copy.deepcopy(self.memory._memory)

        backups = self.memory._memory.setdefault("backups", [])
        backups.append({
            "timestamp": datetime.utcnow().isoformat(),
            "snapshot": snapshot
        })

        self.memory.log_event(
            event="backup_created",
            summary=f"Backup #{len(backups) - 1} creado"
        )

        return snapshot

    def _restore_backup(self, snapshot: dict):
        self.memory._memory.clear()
        self.memory._memory.update(copy.deepcopy(snapshot))