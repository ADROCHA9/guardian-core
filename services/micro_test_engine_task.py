import time
import threading
from services.secure_microtest_sandbox import SecureMicroTestSandbox


class MicroTestEngineTask:
    """
    Ejecuta micro-tests cognitivos reales.

    - Aplica heurísticas antes de ejecutar
    - Ajusta intensidad cognitiva
    - Puede reescribir código con criterio
    - CPU-safe
    - Nunca rompe el loop
    """

    MAX_EXEC_TIME = 0.2  # CPU-safe

    def __init__(self, memory, concept_updater, load_regulator=None):
        self.memory = memory
        self.concept_updater = concept_updater
        self.load_regulator = load_regulator
        self.sandbox = SecureMicroTestSandbox()

    # =================================================
    # API PRINCIPAL
    # =================================================
    def run(self, test_def: dict) -> dict:
        start = time.time()

        result = {
            "passed": False,
            "error": None,
            "explanation": "",
            "timestamp": start,
            "heuristic_warnings": [],
            "rewritten": False
        }

        # -------------------------------------------------
        # 1️⃣ APLICAR HEURÍSTICAS
        # -------------------------------------------------
        warnings, rewritten_code = self._apply_heuristics(test_def)

        if warnings:
            result["heuristic_warnings"] = warnings

        if rewritten_code:
            test_def = dict(test_def)
            test_def["code"] = rewritten_code
            result["rewritten"] = True

        # -------------------------------------------------
        # 2️⃣ EJECUCIÓN REAL (SANDBOX SEGURO)
        # -------------------------------------------------
        def _execute():
            try:
                output = self.sandbox.execute(
                    test_def["code"],
                    test_def["expect"]
                )

                if output == test_def["expected"]:
                    result["passed"] = True
                    result["explanation"] = (
                        "Resultado correcto en sandbox seguro."
                    )
                else:
                    result["explanation"] = (
                        f"Esperado {test_def['expected']} "
                        f"pero se obtuvo {output}."
                    )

            except Exception as e:
                result["error"] = str(e)
                result["explanation"] = "Error en sandbox seguro."

        thread = threading.Thread(target=_execute, daemon=True)
        thread.start()
        thread.join(self.MAX_EXEC_TIME)

        # -------------------------------------------------
        # 3️⃣ ACTUALIZAR CONCEPTOS
        # -------------------------------------------------
        try:
            self.concept_updater.update_from_test(
                test_def.get("concepts", []),
                result
            )
        except Exception:
            # Nunca romper el loop por un error cognitivo
            pass

        # -------------------------------------------------
        # 4️⃣ AJUSTAR INTENSIDAD COGNITIVA
        # -------------------------------------------------
        if self.load_regulator:
            cycle_time = time.time() - start
            try:
                self.load_regulator.run(
                    cycle_time=cycle_time,
                    active_tasks=1,
                    error_count=0 if result["passed"] else 1
                )
            except Exception:
                pass

        return result

    # =================================================
    # HEURÍSTICAS + REESCRITURA
    # =================================================
    def _apply_heuristics(self, test_def: dict):
        """
        Consulta heurísticas aprendidas.
        Puede:
        - advertir
        - reescribir código
        """
        cognitive = self.memory._memory.get("cognitive_memory", {})
        heuristics = cognitive.get("error_heuristics", [])

        warnings = []
        rewritten_code = None

        code = test_def.get("code", "")
        code_lower = code.lower()

        for h in heuristics:
            if not h.get("active", True):
                continue

            etype = h.get("when_error_type")
            suggestion = h.get("suggestion")

            # 🔁 OFF-BY-ONE → REESCRITURA REAL
            if etype == "off-by-one" and "range(len" in code_lower:
                warnings.append(suggestion)
                rewritten_code = self._rewrite_off_by_one(code)

            # 🔁 TYPE MISMATCH → ADVERTENCIA
            elif etype == "type-mismatch":
                warnings.append(suggestion)

            # 🔁 RECURSIÓN SIN BASE
            elif etype == "missing-base-case":
                warnings.append(suggestion)

        if warnings:
            self._log_heuristic_application(warnings, test_def)

        return warnings, rewritten_code

    # =================================================
    # REESCRITURAS SEGURAS
    # =================================================
    def _rewrite_off_by_one(self, code: str) -> str:
        """
        Reescritura segura:
        range(len(x)) → iteración directa
        """
        lines = code.splitlines()
        rewritten = []

        for line in lines:
            if "for i in range(len(" in line:
                rewritten.append(
                    "# Heurística aplicada: evitar índices"
                )
                rewritten.append(
                    line.replace(
                        "for i in range(len(",
                        "for value in "
                    ).replace("):", ":")
                )
            else:
                rewritten.append(line)

        return "\n".join(rewritten)

    # =================================================
    # LOG COGNITIVO
    # =================================================
    def _log_heuristic_application(self, warnings, test_def):
        try:
            self.memory.log_event(
                event="heuristic_applied",
                summary=(
                    f"Heurísticas aplicadas {warnings} "
                    f"antes del test {test_def.get('concepts')}"
                )
            )
            self.memory._persist()
        except Exception:
            pass