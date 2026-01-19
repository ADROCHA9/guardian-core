"""
Adaptador canónico de ProjectMemory para servicios.
NO duplica memoria.
NO rompe imports existentes.
"""

from memory import ProjectMemory


class MemoryAdapter(ProjectMemory):
    """
    Garantiza:
    - root_path
    - _memory
    - compatibilidad total con servicios/*
    """

    def __init__(self, root_path: str):
        super().__init__(root_path)

    @property
    def root_path(self):
        return self.root_path
