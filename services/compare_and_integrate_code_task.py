from typing import Dict, Any, List
from datetime import datetime
import ast


class CompareAndIntegrateCodeTask:
    """
    Tarea cognitiva:
    - Analiza código externo
    - Lo compara con el código propio del Guardian
    - Decide si aporta valor real
    - Genera una propuesta razonada (NO ejecuta)
    """

    def __init__(self, memory, external_code: str):
        self.memory = memory
        self.external_code = external_code

    # =================================================
    # API PRINCIPAL
    # =================================================
    def run(self) -> Dict[str, Any]:
        own_code_index = self._index_own_code()
        external_summary = self._analyze_external_code()

        comparison = self._compare(external_summary, own_code_index)
        decision = self._decide(comparison)

        proposal = {
            "timestamp": datetime.utcnow().isoformat(),
            "external_summary": external_summary,
            "comparison": comparison,
            "decision": decision["decision"],
            "reason": decision["reason"],
            "recommended_action": decision["action"],
            "requires_human_confirmation": True,
            "auto_execute": False
        }

        self._store_proposal(proposal)

        return {
            "decision": decision["decision"],
            "proposal": proposal
        }

    # =================================================
    # ANALIZAR CÓDIGO EXTERNO
    # =================================================
    def _analyze_external_code(self) -> Dict[str, Any]:
        try:
            tree = ast.parse(self.external_code)
        except SyntaxError:
            return {
                "type": "invalid_code",
                "reason": "El código no es sintácticamente válido."
            }

        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return {
            "type": "code",
            "functions": functions,
            "classes": classes,
            "lines": len(self.external_code.splitlines()),
        }

    # =================================================
    # INDEXAR CÓDIGO PROPIO
    # =================================================
    def _index_own_code(self) -> List[str]:
        files = self.memory.get("files", {})
        index = []

        for path, meta in files.items():
            for fn in meta.get("functions", []):
                index.append(fn)
            for cls in meta.get("classes", []):
                index.append(cls)

        return index

    # =================================================
    # COMPARACIÓN
    # =================================================
    def _compare(self, external: Dict[str, Any], own_index: List[str]) -> Dict[str, Any]:
        if external.get("type") != "code":
            return {
                "compatible": False,
                "reason": "No es código válido."
            }

        overlaps = []
        for name in external.get("functions", []) + external.get("classes", []):
            if name in own_index:
                overlaps.append(name)

        return {
            "overlaps": overlaps,
            "is_redundant": bool(overlaps),
            "novelty": "high" if not overlaps else "low"
        }

    # =================================================
    # DECISIÓN CONSCIENTE
    # =================================================
    def _decide(self, comparison: Dict[str, Any]) -> Dict[str, str]:
        if not comparison.get("compatible", True):
            return {
                "decision": "reject",
                "action": "ignore",
                "reason": "El contenido no es código válido."
            }

        if comparison["is_redundant"]:
            return {
                "decision": "compare_and_improve",
                "action": "analyze_existing_code",
                "reason": (
                    "Existe funcionalidad similar. "
                    "Conviene comparar calidad antes de integrar."
                )
            }

        return {
            "decision": "propose_integration",
            "action": "create_new_module",
            "reason": (
                "No existe funcionalidad equivalente. "
                "Puede integrarse como módulo nuevo, tras revisión."
            )
        }

    # =================================================
    # MEMORIA
    # =================================================
    def _store_proposal(self, proposal: Dict[str, Any]) -> None:
        self.memory._memory.setdefault(
            "cognitive_memory", {}
        ).setdefault(
            "code_comparisons", []
        ).append(proposal)

        self.memory._persist()