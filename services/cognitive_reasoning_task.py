from typing import Dict, Any, Optional
from datetime import datetime
import re

from services.evaluate_practical_utility_task import EvaluatePracticalUtilityTask


class CognitiveReasoningTask:
    """
    Razonamiento cognitivo con evaluación de utilidad real (v3).
    """

    def __init__(
        self,
        memory,
        input_text: str,
        context_object: Optional[Dict[str, Any]] = None
    ):
        self.memory = memory
        self.input_text = input_text.strip()
        self.context = context_object

    # =================================================
    # API PRINCIPAL
    # =================================================
    def run(self) -> Dict[str, Any]:
        target = self._resolve_target()

        # 🔍 NUEVO: evaluar utilidad real
        utility = EvaluatePracticalUtilityTask(
            self.memory,
            self.input_text
        ).run()

        signals = self._analyze_content(self.input_text)

        reasoning = {
            "what_it_is": self._what_it_is(target, signals),
            "utility": utility["overall_utility"],
            "value": self._value(target, signals, utility),
            "risks": self._risks(target, signals, utility),
            "architecture_fit": self._architecture_fit(target, signals),
            "decision": ""
        }

        reasoning["decision"] = self._final_decision(reasoning, utility)

        self._persist_reasoning(reasoning, target)

        return {
            "decision": {
                "action": "respond_with_reasoning",
                "timestamp": datetime.utcnow().isoformat()
            },
            "reasoning": reasoning
        }

    # =================================================
    # CONTEXTO
    # =================================================
    def _resolve_target(self) -> Dict[str, Any]:
        if self.context:
            return {"type": "context_object", "data": self.context}

        mem = self.memory._memory
        cmds = mem.get("cognitive_memory", {}).get("cmd_history", [])
        if cmds:
            return {"type": "cmd", "data": cmds[-1]}

        proposals = mem.get("proposed_connections", [])
        if proposals:
            return {"type": "proposal", "data": proposals[-1]}

        return {"type": "text", "data": self.input_text}

    # =================================================
    # ANÁLISIS DE CONTENIDO
    # =================================================
    def _analyze_content(self, text: str) -> Dict[str, bool]:
        return {
            "has_code": bool(re.search(r"\b(def|class)\b", text)),
            "is_trivial": len(text) < 80,
            "is_question": text.endswith("?"),
            "mentions_gui": "gui" in text.lower(),
            "mentions_performance": any(
                k in text.lower()
                for k in ["rápido", "performance", "arranque", "lento"]
            ),
            "mentions_core": any(
                k in text.lower()
                for k in ["núcleo", "cognitivo", "orquestador"]
            ),
        }

    # =================================================
    # RAZONAMIENTO
    # =================================================
    def _what_it_is(self, target, s) -> str:
        if s["has_code"]:
            return "Código propuesto para evaluación técnica."
        if s["is_question"]:
            return "Pedido de análisis o explicación."
        return "Idea conceptual."

    def _value(self, target, s, u) -> str:
        if u["overall_utility"] == "high_util":
            return "Aporta valor práctico claro al sistema."
        if u["overall_utility"] == "medium_util":
            return "Aporta valor potencial, no inmediato."
        if u["overall_utility"] == "low_util":
            return "Valor bajo; no resuelve un problema real."
        return "No aporta valor práctico."

    def _risks(self, target, s, u) -> str:
        if u["overall_utility"] == "high_util" and s["mentions_performance"]:
            return "Riesgo de inestabilidad si se aplica sin métricas."
        if u["overall_utility"] in ("low_util", "no_util"):
            return "Riesgo de ruido arquitectónico."
        return "Riesgo bajo."

    def _architecture_fit(self, target, s) -> str:
        if s["mentions_gui"]:
            return "No pertenece al núcleo cognitivo."
        if s["mentions_core"]:
            return "Impacta el núcleo; requiere revisión humana."
        if s["has_code"]:
            return "Podría ser módulo auxiliar o servicio."
        return "No requiere integración estructural."

    # =================================================
    # DECISIÓN FINAL
    # =================================================
    def _final_decision(self, r, u) -> str:
        util = u["overall_utility"]

        if util in ("no_util", "low_util"):
            return "No integrar. Mantener como referencia o descartar."

        if util == "medium_util":
            return "No ejecutar ahora. Requiere mayor definición."

        if util == "high_util":
            return "Candidato a propuesta estructurada (no ejecutar aún)."

        return "No ejecutar."

    # =================================================
    # MEMORIA
    # =================================================
    def _persist_reasoning(self, reasoning, target) -> None:
        mem = self.memory._memory.setdefault("cognitive_memory", {})
        mem.setdefault("reasoning_history", []).append({
            "timestamp": datetime.utcnow().isoformat(),
            "input": self.input_text,
            "target_type": target["type"],
            "reasoning": reasoning
        })
        self.memory._persist()