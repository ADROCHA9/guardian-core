import tkinter as tk
from tkinter import ttk

from gui.theme import THEME


class MemoryInspectorPanel(tk.Frame):
    """
    Inspector visual READ-ONLY de la memoria del Guardian.
    Permite navegar todo el estado interno de forma segura.
    """

    def __init__(self, parent, memory):
        super().__init__(parent, bg=THEME["panel_bg"])
        self.memory = memory
        self._build()
        self._load_memory()

    # =================================================
    # UI
    # =================================================
    def _build(self):
        header = tk.Label(
            self,
            text="🧠 Inspector de Memoria",
            bg=THEME["panel_bg"],
            fg=THEME["accent"],
            font=THEME["font_main"]
        )
        header.pack(anchor="w", padx=10, pady=6)

        # Treeview
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)

        # Scroll
        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

        # Botón refrescar
        refresh_btn = tk.Button(
            self,
            text="Actualizar memoria",
            command=self._refresh
        )
        refresh_btn.pack(anchor="e", padx=10, pady=6)

    # =================================================
    # CARGA DE MEMORIA
    # =================================================
    def _load_memory(self):
        self.tree.delete(*self.tree.get_children())

        root_id = self.tree.insert(
            "",
            "end",
            text="memory",
            open=True
        )

        self._populate_tree(root_id, self.memory._memory)

    def _populate_tree(self, parent, data):
        """
        Poblado recursivo del árbol.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                node_id = self.tree.insert(
                    parent,
                    "end",
                    text=str(key),
                    open=False
                )
                self._populate_tree(node_id, value)

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                node_id = self.tree.insert(
                    parent,
                    "end",
                    text=f"[{idx}]",
                    open=False
                )
                self._populate_tree(node_id, item)

        else:
            # Valor final
            self.tree.insert(
                parent,
                "end",
                text=repr(data),
                open=False
            )

    # =================================================
    # ACCIONES
    # =================================================
    def _refresh(self):
        self._load_memory()