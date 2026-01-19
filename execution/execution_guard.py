from typing import Dict


class ExecutionGuard:
    def __init__(self, memory_snapshot: Dict):
        self.capabilities = memory_snapshot.get("capabilities", {
            "execution_level": 0
        })

    def can_simulate(self) -> bool:
        return self.capabilities.get("execution_level", 0) >= 1

    def can_execute(self) -> bool:
        return self.capabilities.get("execution_level", 0) >= 2

    def require_confirmation(self) -> bool:
        return self.capabilities.get("execution_level", 0) == 2