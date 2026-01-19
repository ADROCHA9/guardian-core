# execution/sandbox_manager.py
import os
import shutil
import tempfile


class SandboxManager:
    def __init__(self, project_root):
        self.project_root = project_root
        self.sandbox_root = tempfile.mkdtemp(prefix="guardian_sandbox_")

    def create(self):
        def ignore(path, names):
            return {
                name for name in names
                if name.startswith(".project_knowledge.json")
            }

        shutil.copytree(
            self.project_root,
            self.sandbox_root,
            dirs_exist_ok=True,
            ignore=ignore
        )

        return self.sandbox_root