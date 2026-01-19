# memory.py

import json
import os
import threading
from datetime import datetime
from typing import Any, Dict

# =====================================================
# LOCK GLOBAL ÚNICO (CRÍTICO PARA WINDOWS)
# =====================================================
_MEMORY_LOCK = threading.Lock()


class ProjectMemory:
    """
    Memoria canónica del Guardian.
    THREAD-SAFE.
    """

    # =====================================================
    # ROOT CANÓNICO MULTI-PLATAFORMA (IDENTIDAD PROTEGIDA)
    # =====================================================
    if os.name == "nt":
        ROOT_CANONICO = r"C:\Users\CONECTIA BA\guardian_bot"
    else:
        ROOT_CANONICO = "/home/adrian/guardian_bot"

    def __init__(self, root_path: str):
        root_path = os.path.abspath(root_path)

        if root_path != self.ROOT_CANONICO:
            raise RuntimeError(
                "\n[FATAL] Guardian detectó memoria fuera de su root.\n"
                f"Root recibido : {root_path}\n"
                f"Root permitido: {self.ROOT_CANONICO}\n"
                "Se aborta para preservar identidad y conciencia.\n"
            )

        self.root_path = root_path
        self.memory_file = os.path.join(
            self.root_path, ".project_knowledge.json"
        )

        self._memory: Dict[str, Any] = {}

    # =====================================================
    # CARGA / INICIALIZACIÓN
    # =====================================================
    def load(self) -> None:
        if not os.path.exists(self.memory_file):
            self._initialize_memory()
            self._persist()
            return

        with open(self.memory_file, "r", encoding="utf-8") as f:
            self._memory = json.load(f)

        self._migrate_memory()
        self._persist()

    def _initialize_memory(self) -> None:
        self._memory = {
            # -------------------------
            # PROYECTO ACTIVO
            # -------------------------
            "project": {
                "name": "NICONO",
                "version_label": "v3.0",
                "root_path": self.root_path,
                "purpose": "Sistema orquestador soberano, guardián, perpetuo y evolutivo",
                "domain": "software / orquestación / conciencia sistémica",
                "created_at": self._now(),
                "last_scan": None,
                "version": "0.1"
            },

            # -------------------------
            # IDENTIDAD
            # -------------------------
            "identity": {},

            # -------------------------
            # ESTADO DEL GUARDIAN
            # -------------------------
            "guardian_self": {
                "identity": "Guardian",
                "operator": None,
                "authority_model": "human_in_the_loop",
                "evolution_level": 0,
                "status": "stable",
                "ready_for_execution": False
            },

            # -------------------------
            # CONCIENCIA
            # -------------------------
            "conscious_state": {
                "active": True,
                "mode": "vigilante",
                "assumption_policy": "ask_before_assume",
                "confidence_level": "structural"
            },

            # -------------------------
            # CAPACIDADES
            # -------------------------
            "capabilities": {
                "execution_level": 0,
                "can_self_modify": False,
                "can_manage_hardware": False,
                "can_manage_nodes": False
            },

            # -------------------------
            # ENTORNO / SERVICIOS / NODOS
            # -------------------------
            "environment": {},
            "services": {},
            "nodes": {},

            # -------------------------
            # CONSENTIMIENTOS
            # -------------------------
            "consents": [],

            # -------------------------
            # CONOCIMIENTO DEL PROYECTO
            # -------------------------
            "files": {},
            "relations": [],
            "inconsistencies": [],
            "proposed_connections": [],
            "open_questions": [],

            # -------------------------
            # HISTORIA EVOLUTIVA
            # -------------------------
            "evolution_log": [],
            "evolution_decisions": [],

            # -------------------------
            # MEMORIA COGNITIVA
            # -------------------------
            "cognitive_memory": {
                "decisions": [],
                "preferences": {},
                "patterns": [],
                "gui_hints": [],
                "raw_ideas": [],
                "tasks": []
            }
        }

    def _migrate_memory(self) -> None:
        defaults = {
            "identity": {},
            "guardian_self": {},
            "conscious_state": {},
            "capabilities": {},
            "environment": {},
            "services": {},
            "nodes": {},
            "consents": [],
            "files": {},
            "relations": [],
            "inconsistencies": [],
            "proposed_connections": [],
            "open_questions": [],
            "evolution_log": [],
            "evolution_decisions": [],
            "cognitive_memory": {
                "decisions": [],
                "preferences": {},
                "patterns": [],
                "gui_hints": [],
                "raw_ideas": [],
                "tasks": []
            }
        }

        for key, default in defaults.items():
            if key not in self._memory:
                self._memory[key] = default

    # =====================================================
    # UTILIDADES
    # =====================================================
    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    # =====================================================
    # PERSISTENCIA THREAD-SAFE
    # =====================================================
    def _persist(self) -> None:
        with _MEMORY_LOCK:
            tmp_file = self.memory_file + ".tmp"
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(self._memory, f, indent=2, ensure_ascii=False)
            os.replace(tmp_file, self.memory_file)

    # =====================================================
    # GETTERS
    # =====================================================
    def get(self, section: str, default: Any = None) -> Any:
        return self._memory.get(section, default)

    def get_file(self, file_path: str) -> Dict[str, Any]:
        return self._memory.get("files", {}).get(file_path, {})

    # =====================================================
    # ESCRITURA CONTROLADA
    # =====================================================
    def update_project_scan_time(self) -> None:
        self._memory["project"]["last_scan"] = self._now()
        self._persist()

    def register_file(self, file_path: str, data: Dict[str, Any]) -> None:
        self._memory["files"][file_path] = data
        self._persist()

    def add_relation(self, relation: Dict[str, Any]) -> None:
        self._memory["relations"].append(relation)
        self._persist()

    def add_inconsistency(self, issue: Dict[str, Any]) -> None:
        self._memory["inconsistencies"].append(issue)
        self._persist()

    def add_proposed_connection(self, proposal: Dict[str, Any]) -> None:
        self._memory["proposed_connections"].append(proposal)
        self._persist()

    def add_question(self, question: Dict[str, Any]) -> None:
        self._memory["open_questions"].append(question)
        self._persist()

    # =====================================================
    # MÉTODOS CLAVE
    # =====================================================
    def set_environment(self, environment_state: Dict[str, Any]) -> None:
        self._memory["environment"] = environment_state
        self._persist()

    def register_node(self, node_id: str, node_profile: Dict[str, Any]) -> None:
        self._memory["nodes"][node_id] = node_profile
        self._persist()

    def register_consent(self, consent: Dict[str, Any]) -> None:
        self._memory["consents"].append(consent)
        self._persist()

    def update_guardian_state(self, updates: Dict[str, Any]) -> None:
        self._memory["guardian_self"].update(updates)
        self._persist()

    def set_active_project(self, project: dict) -> None:
        self._memory["project"] = project
        self._persist()

    def log_event(self, event: str, summary: str) -> None:
        self._memory["evolution_log"].append({
            "timestamp": self._now(),
            "event": event,
            "summary": summary
        })
        self._persist()
