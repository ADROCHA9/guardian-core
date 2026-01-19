import os


class RootIntegrityLockTask:
    """
    Bloquea la carpeta raíz del Guardian contra modificaciones externas.
    """

    def __init__(self, root_path, memory):
        self.root = root_path
        self.memory = memory

    def enforce(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        guardian["root_locked"] = True
        guardian["root_path_hash"] = hash(os.path.abspath(self.root))
        self.memory._persist()