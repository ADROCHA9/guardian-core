from datetime import datetime


class ModuleRefactorProposalTask:
    """
    Propone integrar, unificar o eliminar módulos.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        classified = self.memory._memory.get("cognitive_memory", {}).get("classified_modules")
        if not classified:
            return None

        proposals = []

        for m in classified["modules"]:
            if m["classification"] == "obsolete":
                proposals.append({
                    "action": "remove",
                    "path": m["path"],
                    "reason": "Módulo obsoleto"
                })
            elif m["classification"] == "isolated":
                proposals.append({
                    "action": "integrate",
                    "path": m["path"],
                    "reason": "Función aislada integrable"
                })

        self.memory._memory["cognitive_memory"]["module_refactor_proposals"] = {
            "generated_at": datetime.utcnow().isoformat(),
            "proposals": proposals
        }

        self.memory._persist()
        return proposals