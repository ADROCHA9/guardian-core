import copy
import traceback
from datetime import datetime


class SandboxManager:
    """
    Ejecuta propuestas en entorno aislado (sandbox).
    NO toca memoria real.
    Genera reportes comparativos.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self, proposal: dict) -> dict:
        """
        Ejecuta una propuesta en sandbox y devuelve reporte.
        """
        snapshot_before = copy.deepcopy(self.memory._memory)

        report = {
            "proposal_id": proposal.get("id"),
            "started_at": datetime.utcnow().isoformat(),
            "status": "unknown",
            "effects": {},
            "errors": None
        }

        try:
            effects = self._simulate(proposal, snapshot_before)
            report["status"] = "success"
            report["effects"] = effects
        except Exception as e:
            report["status"] = "failed"
            report["errors"] = traceback.format_exc()

        report["finished_at"] = datetime.utcnow().isoformat()
        return report

    # =================================================
    # SIMULACIÓN
    # =================================================
    def _simulate(self, proposal, snapshot):
        """
        Simula efectos lógicos sin persistir cambios.
        """
        effects = {
            "files_delta": 0,
            "relations_delta": 0,
            "inconsistencies_delta": 0,
            "notes": []
        }

        if proposal.get("type") == "new_module":
            effects["files_delta"] += 1
            effects["notes"].append("Se agregaría un nuevo módulo.")

        if proposal.get("type") == "refactor":
            effects["relations_delta"] += 1
            effects["notes"].append("Se reorganizarían relaciones internas.")

        if proposal.get("type") == "cleanup":
            effects["inconsistencies_delta"] -= 1
            effects["notes"].append("Se reducirían inconsistencias.")

        return effects