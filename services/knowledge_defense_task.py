from datetime import datetime
import hashlib
import json


class KnowledgeDefenseTask:
    """
    Defiende el conocimiento de Guardian ante cambios:
    - Detecta degradación
    - Detecta contradicciones
    - Registra intentos de modificación riesgosa
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        guardian = self.memory._memory.setdefault("guardian_self", {})
        cognitive = self.memory._memory.get("cognitive_memory", {})

        previous = guardian.get("last_knowledge_snapshot")
        current_hash = self._hash(cognitive)

        if previous:
            if previous["hash"] != current_hash:
                # Cambio detectado
                defense = {
                    "detected_at": datetime.utcnow().isoformat(),
                    "previous_hash": previous["hash"],
                    "current_hash": current_hash,
                    "action": "allowed",
                    "reason": "Cambio cognitivo detectado"
                }

                # Defensa: evitar regresión fuerte
                if self._is_regression(previous["snapshot"], cognitive):
                    defense["action"] = "blocked"
                    defense["reason"] = "Posible regresión cognitiva detectada"

                guardian.setdefault("knowledge_defense_log", []).append(defense)

                self.memory.log_event(
                    event="knowledge_defense",
                    summary=f"Cambio cognitivo → {defense['action']}"
                )

        guardian["last_knowledge_snapshot"] = {
            "hash": current_hash,
            "snapshot": self._light_snapshot(cognitive),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.memory._persist()

    # =============================
    # INTERNOS
    # =============================
    def _hash(self, data):
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def _light_snapshot(self, cognitive):
        """
        Snapshot liviano (no duplica memoria).
        """
        return {
            "concepts": list(cognitive.get("concepts", {}).keys()),
            "heuristics": len(cognitive.get("error_heuristics", [])),
            "patterns": len(cognitive.get("error_patterns", []))
        }

    def _is_regression(self, previous, current):
        """
        Detecta pérdida clara de capacidad.
        """
        prev_concepts = set(previous.get("concepts", []))
        curr_concepts = set(current.get("concepts", {}).keys())

        # Pérdida significativa de conceptos
        return len(curr_concepts) < len(prev_concepts) * 0.7