from collections import Counter, defaultdict
from datetime import datetime, timedelta
import time


class ErrorPatternMiningTask:
    """
    Analiza errores reales del Guardian y construye:
    - Patrones semánticos de error
    - Heurísticas preventivas
    - Decaimiento inteligente de patrones obsoletos

    Esta tarea REDUCE errores futuros.
    """

    # ================= CONFIGURACIÓN =================

    MIN_OCCURRENCES = 3          # mínimo para considerar patrón
    DECAY_DAYS = 14              # días sin aparecer → decaimiento
    MAX_PATTERNS = 50            # límite duro (memoria ligera)

    # Tipificación semántica básica (extensible)
    ERROR_TYPES = {
        "off-by-one": ["index", "range", "len", "i+1", "i - 1"],
        "type-mismatch": ["TypeError", "str", "int", "None"],
        "wrong-iteration-target": ["range(len", "index"],
        "missing-base-case": ["recursion", "maximum recursion"],
        "division-by-zero": ["ZeroDivisionError", "/ 0"]
    }

    # ================= INIT =================

    def __init__(self, memory):
        self.memory = memory

    # ================= API PRINCIPAL =================

    def run(self):
        """
        Ejecuta minería completa:
        - detecta errores
        - agrupa patrones
        - genera heurísticas
        - limpia patrones obsoletos
        """
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        events = self.memory._memory.get("evolution_log", [])

        error_events = self._extract_error_events(events)
        if not error_events:
            return []

        typed_errors = self._classify_errors(error_events)
        pattern_stats = self._count_patterns(typed_errors)

        patterns = cognitive.setdefault("error_patterns", [])
        heuristics = cognitive.setdefault("error_heuristics", [])

        new_patterns = self._update_patterns(
            patterns,
            heuristics,
            pattern_stats
        )

        self._decay_patterns(patterns)
        self._enforce_limits(patterns, heuristics)

        self.memory._persist()
        return new_patterns

    # ================= EXTRACCIÓN =================

    def _extract_error_events(self, events):
        """
        Extrae eventos que representan errores reales.
        """
        results = []
        for e in events:
            summary = e.get("summary", "").lower()
            if "error" in summary or "exception" in summary:
                results.append({
                    "summary": summary,
                    "timestamp": e.get("timestamp")
                })
        return results

    # ================= CLASIFICACIÓN =================

    def _classify_errors(self, error_events):
        """
        Asigna tipo semántico a cada error.
        """
        classified = []
        for e in error_events:
            error_type = self._infer_error_type(e["summary"])
            classified.append({
                "type": error_type,
                "summary": e["summary"],
                "timestamp": e["timestamp"]
            })
        return classified

    def _infer_error_type(self, text: str) -> str:
        for etype, keywords in self.ERROR_TYPES.items():
            for k in keywords:
                if k.lower() in text:
                    return etype
        return "unknown"

    # ================= AGRUPACIÓN =================

    def _count_patterns(self, typed_errors):
        """
        Cuenta ocurrencias por tipo de error.
        """
        counter = Counter(e["type"] for e in typed_errors)
        last_seen = {}

        for e in typed_errors:
            last_seen[e["type"]] = e["timestamp"]

        return {
            "counts": counter,
            "last_seen": last_seen
        }

    # ================= ACTUALIZACIÓN =================

    def _update_patterns(self, patterns, heuristics, stats):
        """
        Actualiza patrones existentes o crea nuevos.
        """
        new_patterns = []
        now = datetime.utcnow().isoformat()

        for etype, count in stats["counts"].items():
            if count < self.MIN_OCCURRENCES:
                continue

            existing = self._find_pattern(patterns, etype)

            if existing:
                existing["occurrences"] += count
                existing["last_seen"] = stats["last_seen"].get(etype)
            else:
                pattern = {
                    "type": etype,
                    "occurrences": count,
                    "created_at": now,
                    "last_seen": stats["last_seen"].get(etype),
                    "active": True
                }
                patterns.append(pattern)
                new_patterns.append(pattern)

                heuristic = self._build_heuristic(etype)
                if heuristic:
                    heuristics.append(heuristic)

        return new_patterns

    def _find_pattern(self, patterns, etype):
        for p in patterns:
            if p.get("type") == etype:
                return p
        return None

    # ================= HEURÍSTICAS =================

    def _build_heuristic(self, etype):
        """
        Convierte patrón en regla preventiva.
        """
        suggestions = {
            "off-by-one": "Evitar índices explícitos. Preferir iteración directa.",
            "type-mismatch": "Validar tipos antes de operar.",
            "wrong-iteration-target": "Iterar sobre valores, no índices.",
            "missing-base-case": "Asegurar caso base en recursión.",
            "division-by-zero": "Verificar divisor distinto de cero."
        }

        suggestion = suggestions.get(etype)
        if not suggestion:
            return None

        return {
            "when_error_type": etype,
            "suggestion": suggestion,
            "created_at": datetime.utcnow().isoformat(),
            "active": True
        }

    # ================= DECAIMIENTO =================

    def _decay_patterns(self, patterns):
        """
        Desactiva patrones que no aparecen hace tiempo.
        """
        now = datetime.utcnow()
        for p in patterns:
            last = p.get("last_seen")
            if not last:
                continue

            try:
                last_dt = datetime.fromisoformat(last)
            except Exception:
                continue

            if now - last_dt > timedelta(days=self.DECAY_DAYS):
                p["active"] = False

    # ================= LÍMITES =================

    def _enforce_limits(self, patterns, heuristics):
        """
        Mantiene memoria ligera.
        """
        if len(patterns) > self.MAX_PATTERNS:
            patterns[:] = sorted(
                patterns,
                key=lambda p: p.get("occurrences", 0),
                reverse=True
            )[:self.MAX_PATTERNS]

        if len(heuristics) > self.MAX_PATTERNS:
            heuristics[:] = heuristics[:self.MAX_PATTERNS]
