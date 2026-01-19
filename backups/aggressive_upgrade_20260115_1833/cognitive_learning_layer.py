# services/cognitive_learning_layer.py

from datetime import datetime
from typing import Dict, List


# ================= CONFIGURACIÓN COGNITIVA =================

MAX_DECISIONS = 50          # memoria explícita acotada
MAX_GUI_HINTS = 30          # hints GUI activos
MAX_RAW_IDEAS = 40          # ideas no consolidadas
DECAY_SECONDS = 60 * 60     # 1 hora de relevancia


class CognitiveLearningLayer:
    """
    Capa de aprendizaje explícito y mapeo cognitivo → GUI.
    También mantiene el sistema liviano (limpieza cognitiva).
    """

    def __init__(self, memory):
        self.memory = memory
        self._ensure_structures()

    # =====================================================
    # INICIALIZACIÓN SEGURA
    # =====================================================
    def _ensure_structures(self):
        self.memory._memory.setdefault("cognitive_memory", {})
        cm = self.memory._memory["cognitive_memory"]

        cm.setdefault("decisions", [])
        cm.setdefault("preferences", {})
        cm.setdefault("patterns", [])
        cm.setdefault("gui_hints", [])
        cm.setdefault("raw_ideas", [])

    # =====================================================
    # PROCESAMIENTO PRINCIPAL
    # =====================================================
    def process(self, core_result: Dict, human_input: str | None) -> Dict:
        """
        Enriquecer salida del cerebro con:
        - aprendizaje explícito
        - mapeo a GUI
        - limpieza cognitiva
        """
        cm = self.memory._memory["cognitive_memory"]

        # ----------------- 1️⃣ Aprendizaje explícito -----------------
        if human_input and core_result.get("mode") == "learning":
            self._record_decision(
                input_text=human_input,
                reason="interacción directa con el operador"
            )

        # ----------------- 2️⃣ Mapear a GUI -----------------
        gui_hints = self._extract_gui_hints(human_input)
        if gui_hints:
            cm["gui_hints"].extend(gui_hints)

        # ----------------- 3️⃣ Guardar ideas crudas (temporal) -----------------
        ideas = core_result.get("ideas", [])
        for idea in ideas:
            cm["raw_ideas"].append({
                "idea": idea,
                "timestamp": datetime.utcnow().timestamp()
            })

        # ----------------- 4️⃣ Limpieza cognitiva -----------------
        self._cleanup()

        # ----------------- 5️⃣ Exponer hints y aprendizaje -----------------
        core_result["learning"] = {
            "decisions": len(cm["decisions"]),
            "patterns": list(cm["preferences"].keys())
        }

        core_result["gui_hints"] = list(cm["gui_hints"])

        self.memory._persist()
        return core_result

    # =====================================================
    # APRENDIZAJE EXPLÍCITO
    # =====================================================
    def _record_decision(self, input_text: str, reason: str):
        cm = self.memory._memory["cognitive_memory"]

        decision = {
            "input": input_text,
            "reason": reason,
            "timestamp": datetime.utcnow().timestamp()
        }

        cm["decisions"].append(decision)

        # Extraer preferencias simples (heurística liviana)
        if "ver" in input_text or "visible" in input_text:
            cm["preferences"]["visibility"] = (
                cm["preferences"].get("visibility", 0) + 1
            )

        if "editar" in input_text or "editable" in input_text:
            cm["preferences"]["editability"] = (
                cm["preferences"].get("editability", 0) + 1
            )

    # =====================================================
    # MAPEO A GUI (INTENCIÓN, NO CÓDIGO)
    # =====================================================
    def _extract_gui_hints(self, text: str | None) -> List[Dict]:
        if not text:
            return []

        hints = []

        lowered = text.lower()

        if "ver" in lowered or "mostrar" in lowered:
            hints.append({
                "type": "expose",
                "target": "module",
                "location": "main_or_sidebar",
                "priority": "high"
            })

        if "editar" in lowered:
            hints.append({
                "type": "editable",
                "target": "module",
                "interaction": "form_or_panel"
            })

        return hints

    # =====================================================
    # LIMPIEZA COGNITIVA (ANTI-COLAPSO)
    # =====================================================
    def _cleanup(self):
        now = datetime.utcnow().timestamp()
        cm = self.memory._memory["cognitive_memory"]

        # ---- 1️⃣ Decisiones (FIFO)
        cm["decisions"] = cm["decisions"][-MAX_DECISIONS:]

        # ---- 2️⃣ GUI hints (recientes)
        cm["gui_hints"] = cm["gui_hints"][-MAX_GUI_HINTS:]

        # ---- 3️⃣ Ideas crudas (por tiempo + cantidad)
        cm["raw_ideas"] = [
            i for i in cm["raw_ideas"]
            if now - i["timestamp"] < DECAY_SECONDS
        ]
        cm["raw_ideas"] = cm["raw_ideas"][-MAX_RAW_IDEAS:]