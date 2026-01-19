class TaskEngine:
    def __init__(self, memory):
        self.memory = memory

    def create_task(self, intent: str):
        task = {
            "id": f"task_{int(time.time())}",
            "type": "self_analysis",
            "intent": intent,
            "status": "pending",
            "result": None
        }
        self.memory._memory.setdefault("cognitive_memory", {}).setdefault("tasks", []).append(task)
        self.memory.log_event("task_created", intent)
        self.memory._persist()
        return task