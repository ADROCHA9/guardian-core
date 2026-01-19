from datetime import datetime


class StructuralRedesignProposalTask:
    """
    Propone rediseños estructurales sin ejecutarlos.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        proposal = {
            "proposed_at": datetime.utcnow().isoformat(),
            "proposal": (
                "Separar memoria episódica y memoria de reglas "
                "para mejorar claridad y reducir ruido."
            ),
            "risk": "medio",
            "requires_human_approval": True
        }

        self.memory._memory.setdefault("cognitive_memory", {}).setdefault(
            "structural_proposals", []
        ).append(proposal)

        self.memory._persist()
        return proposal