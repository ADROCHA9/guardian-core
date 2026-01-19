from typing import Dict, Any, Optional
from datetime import datetime
import re


class EvaluatePracticalUtilityTask:
    """
    Evalúa UTILIDAD REAL de una idea o código
    dentro del sistema Guardian.
    """

    def __init__(self, memory, input_text: str):
        self.memory = memory
        self.text = input_text.strip()

    # =================================================
    # API PRINCIPAL
    # =================================================
    def run(self) -> Dict[str, Any]:
        signals = self._analyze_content(self.text)

        utility = {
            "has_clear_purpose": self._has_clear_purpose(signals),
            "solves_existing_problem": self._solves_problem(signals),
            "is_redundant": self._is_redundant(signals),
            "adds_complexity": self._adds_complexity(signals),
            "overall_utility": "",
        }

        utility["overall_utility"] = self._overall_decision(utility)

        self._persist_utility(utility)

        return utility

    # =================================================
    # ANÁLISIS BÁSICO
    # =================================================
    def _analyze_content(self, text: str) -> Dict[str, bool]:
        return {
            "has_code": bool(re.search(r"\b(def|class)\b", text)),
            "is_trivial": len(text) < 80,
            "mentions_performance": any(
                k in text.lower()
                for k in ["rápido", "performance", "arranque", "lento"]
            ),
            "mentions_gui": "gui" in text.lower(),
            "mentions_logging": "log" in text.lower(),
        }

    # =================================================
    # CRITERIOS
    # =================================================
    def _has_clear_purpose(self, s: Dict[str, bool]) -> bool:
        if s["mentions_performance"] or s["mentions_logging"]:
            return True
        if s["has_code"] and not s["is_trivial"]:
            return True
        return False

    def _solves_problem(self, s: Dict[str, bool]) -> bool:
        return s["mentions_performance"] or s["mentions_logging"]

    def _is_redundant(self, s: Dict[str, bool]) -> bool:
        # Placeholder realista:
        # más adelante se compara contra código existente
        return s["is_trivial"]

    def _adds_complexity(self, s: Dict[str, bool]) -> bool:
        return s["mentions_gui"] and not s["mentions_performance"]

    def _overall_decision(self, u: Dict[str, bool]) -> str:
        if not u["has_clear_purpose"]:
            return "no_util"
        if u["is_redundant"]:
            return "low_util"
        if u["solves_existing_problem"]:
            return "high_util"
        return "medium_util"

    # =================================================
    # MEMORIA
    # =================================================
    def _persist_utility(self, utility: Dict[str, Any]) -> None:
        mem = self.memory._memory.setdefault("cognitive_memory", {})
        mem.setdefault("utility_evaluations", []).append({
            "timestamp": datetime.utcnow().isoformat(),
            "input": self.text,
            "utility": utility
        })
        self.memory._persist()