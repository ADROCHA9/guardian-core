import ast
import time
import traceback


class SelfCorrectionAgentTask:
    """
    Agente de auto-corrección.
    Guardian genera código con su conocimiento actual,
    lo analiza, lo ejecuta, aprende o lo descarta.
    """

    def __init__(self, memory, micro_test_engine, concept_updater):
        self.memory = memory
        self.micro_test_engine = micro_test_engine
        self.concept_updater = concept_updater

    # =====================================================
    # 1️⃣ GENERAR CÓDIGO (SOLO CON LO QUE SABE)
    # =====================================================
    def generate_code(self) -> dict:
        """
        Genera un fragmento de código simple basado en
        conceptos dominados o en progreso.
        """
        cognitive = self.memory._memory.get("cognitive_memory", {})
        concepts = cognitive.get("concepts", {})

        # Elegir conceptos con algo de estabilidad
        usable = [
            name for name, c in concepts.items()
            if c.get("level", 0) >= 2
        ]

        if "function" in usable and "addition" in usable:
            code = (
                "def add(a, b):\n"
                "    return a + b\n\n"
                "result = add(2, 3)"
            )
            return {
                "code": code,
                "expect": "result",
                "expected": 5,
                "concepts": ["function", "addition"],
                "purpose": "sumar dos valores"
            }

        return {}

    # =====================================================
    # 2️⃣ ANALIZAR CÓDIGO (SIN EJECUTAR)
    # =====================================================
    def analyze_code(self, code: str) -> dict:
        """
        Analiza sintaxis y estructura.
        """
        analysis = {
            "syntax_ok": False,
            "issues": []
        }

        try:
            tree = ast.parse(code)
            analysis["syntax_ok"] = True

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.body:
                    analysis["issues"].append(
                        "Función definida sin cuerpo."
                    )

        except Exception as e:
            analysis["issues"].append(str(e))

        return analysis

    # =====================================================
    # 3️⃣ EJECUTAR, TESTEAR Y CORREGIR
    # =====================================================
    def run(self):
        generated = self.generate_code()
        if not generated:
            return None  # Nada útil para probar

        code = generated["code"]

        # Análisis estático
        analysis = self.analyze_code(code)
        if not analysis["syntax_ok"]:
            self._learn_failure(
                generated["concepts"],
                "Error de sintaxis",
                analysis["issues"]
            )
            return {
                "status": "discarded",
                "reason": "syntax_error"
            }

        # Micro-test real
        test_result = self.micro_test_engine.run(generated)

        if test_result["passed"]:
            self._learn_success(generated)
            return {
                "status": "accepted",
                "purpose": generated["purpose"]
            }

        # Falló → aprendizaje
        self._learn_failure(
            generated["concepts"],
            test_result.get("error"),
            test_result.get("explanation")
        )

        return {
            "status": "corrected",
            "reason": test_result.get("explanation")
        }

    # =====================================================
    # 4️⃣ APRENDER DE ÉXITOS
    # =====================================================
    def _learn_success(self, generated):
        self.memory.log_event(
            event="self_correction_success",
            summary=f"Código válido para {generated['purpose']}"
        )
        self.memory._persist()

    # =====================================================
    # 5️⃣ APRENDER DE ERRORES
    # =====================================================
    def _learn_failure(self, concepts, error, explanation):
        for c in concepts:
            self.concept_updater.update_from_test(
                [c],
                {"passed": False}
            )

        self.memory.log_event(
            event="self_correction_failure",
            summary=f"Error detectado: {explanation}"
        )
        self.memory._persist()