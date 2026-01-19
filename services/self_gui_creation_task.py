class SelfGuiCreationTask:
    """
    Guardian solo puede proponer su propia GUI cuando domina Tkinter.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        knowledge = self.memory._memory.get("cognitive_memory", {}).get("python_knowledge", {})

        if "tkinter" not in knowledge:
            return None

        proposal = {
            "proposal": "Crear GUI cognitiva modular propia",
            "reason": "Dominio suficiente de Tkinter detectado",
            "status": "proposal_only"
        }

        self.memory._memory.setdefault("guardian_self", {}).setdefault(
            "gui_proposals", []
        ).append(proposal)

        self.memory._persist()
        return proposal