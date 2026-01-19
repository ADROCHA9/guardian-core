from typing import Dict, List
from datetime import datetime


class EvolutionLog:
    def __init__(self, memory: Dict):
        self.memory = memory
        self.memory.setdefault("evolution_decisions", [])

    def record(
        self,
        proposal_id: str,
        action: str,
        result: str,
        details: Dict
    ) -> None:
        self.memory["evolution_decisions"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "proposal_id": proposal_id,
            "action": action,
            "result": result,
            "details": details
        })