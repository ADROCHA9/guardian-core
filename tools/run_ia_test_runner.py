# tools/run_ai_test_runner.py
from memory import ProjectMemory
from execution.sandbox_manager import SandboxManager
from execution.ai_analysis_flow import run_ai_analysis
from execution.ai_to_code_generator import apply_ai_suggestions_to_sandbox
from execution.test_runner import TestRunner


if __name__ == "__main__":
    ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"

    # 1️⃣ Cargar memoria
    memory = ProjectMemory(ROOT)
    memory.load()

    # 2️⃣ Crear sandbox
    sandbox = SandboxManager(ROOT)
    sandbox_path = sandbox.create()

    # 3️⃣ Análisis IA
    analysis = run_ai_analysis(
        task="Proponer mejoras estructurales para el Guardian",
        memory_snapshot=memory._memory
    )

    if not analysis:
        print("❌ No se obtuvo análisis IA.")
        exit(1)

    # 4️⃣ Aplicar sugerencias IA en sandbox
    target_files = ["proposal_engine.py"]
    changes = apply_ai_suggestions_to_sandbox(
        analysis_text=analysis,
        sandbox_path=sandbox_path,
        target_files=target_files
    )

    if not changes:
        print("⚠️ No se generaron cambios en sandbox.")
        exit(0)

    print("\n🧪 CAMBIOS GENERADOS EN SANDBOX")
    for c in changes:
        print(c)

    # 5️⃣ Ejecutar tests automáticos
    runner = TestRunner(sandbox_path)
    results = runner.run_basic_tests(
        files=[c["file"] for c in changes]
    )

    print("\n🔍 RESULTADOS DE TESTS")
    errors = False
    for r in results:
        print(r)
        if r["status"] != "ok":
            errors = True

    # 6️⃣ Resultado final
    if errors:
        print("\n❌ TESTS FALLIDOS. Flujo BLOQUEADO.")
    else:
        print("\n✅ TESTS OK. Listo para DIFF y CONFIRMACIÓN.")