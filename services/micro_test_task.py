class MicroTestTask:
    """
    Ejecuta pruebas lógicas mínimas SIN tocar archivos.
    """

    def __init__(self, memory, proposal: dict):
        self.memory = memory
        self.proposal = proposal

    def run(self) -> dict:
        results = []

        # Test 1: ¿Duplica algo existente?
        existing = self.memory.get("files", {})
        results.append({
            "test": "duplication_check",
            "passed": self.proposal.get("target") not in existing
        })

        # Test 2: ¿Requiere ejecución?
        results.append({
            "test": "execution_required",
            "passed": self.proposal.get("impact") != "alto"
        })

        return {
            "proposal": self.proposal,
            "tests": results,
            "all_passed": all(r["passed"] for r in results)
        }