# services/self_recognition_task.py

import os
from typing import Dict, List


class SelfRecognitionTask:
    """
    Tarea real:
    Guardian recorre su propio código y declara sus partes.
    """

    EXCLUDE_DIRS = {
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        ".idea",
        ".pytest_cache"
    }

    def __init__(self, memory):
        self.memory = memory
        self.root = memory.root_path

    def run(self) -> Dict:
        structure = {
            "root": self.root,
            "modules": [],
            "summary": {}
        }

        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [
                d for d in dirnames if d not in self.EXCLUDE_DIRS
            ]

            for fname in filenames:
                if not fname.endswith(".py"):
                    continue

                full_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(full_path, self.root)

                module_info = self._analyze_file(rel_path, full_path)
                structure["modules"].append(module_info)

        structure["summary"] = self._summarize(structure["modules"])
        return structure

    # =================================================
    # ANALYSIS
    # =================================================
    def _analyze_file(self, rel_path: str, full_path: str) -> Dict:
        role = self._infer_role(rel_path)

        return {
            "file": rel_path,
            "role": role,
        }

    def _infer_role(self, path: str) -> str:
        p = path.lower()

        if "cognitive" in p or "intelligence" in p:
            return "cognitive_core"
        if "memory" in p:
            return "memory"
        if "loop" in p or "orchestr" in p:
            return "orchestration"
        if "gui" in p or "panel" in p:
            return "interface"
        if "execution" in p or "sandbox" in p:
            return "execution_control"
        if "security" in p or "auth" in p:
            return "security"
        if "service" in p:
            return "service"
        return "utility"

    def _summarize(self, modules: List[Dict]) -> Dict:
        summary = {}
        for m in modules:
            summary[m["role"]] = summary.get(m["role"], 0) + 1
        return summary