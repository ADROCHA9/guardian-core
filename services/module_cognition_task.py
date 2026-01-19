from datetime import datetime


class ModuleCognitionTask:
    """
    Decide si un módulo es útil, redundante, aislado o basura.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        data = self.memory._memory.get("cognitive_memory", {}).get("codebase_modules")
        if not data:
            return None

        classified = []

        for m in data["modules"]:
            tag = "useful"
            if m["size"] < 200:
                tag = "isolated"
            if "old" in m["name"] or "tmp" in m["name"]:
                tag = "obsolete"

            classified.append({**m, "classification": tag})

        self.memory._memory["cognitive_memory"]["classified_modules"] = {
            "classified_at": datetime.utcnow().isoformat(),
            "modules": classified
        }

        self.memory._persist()
        return classified