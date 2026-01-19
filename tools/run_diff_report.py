# tools/run_diff_report.py
from memory import ProjectMemory
from execution.sandbox_manager import SandboxManager
from execution.ai_analysis_flow import run_ai_analysis
from execution.ai_to_code_generator import apply_ai_suggestions_to_sandbox
from execution.test_runner import TestRunner
from execution.diff_engine import DiffEngine


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

    # 5️⃣ Ejecutar tests
    runner = TestRunner(sandbox_path)
    results = runner.run_basic_tests(
        files=[c["file"] for c in changes]
    )

    if any(r["status"] != "ok" for r in results):
        print("❌ Tests fallidos. No se genera diff.")
        exit(1)

    # 6️⃣ Generar diff
    diff_engine = DiffEngine(
        project_root=ROOT,
        sandbox_path=sandbox_path
    )

    diffs = diff_engine.run(
        changed_files=[c["file"] for c in changes]
    )

    # 7️⃣ Informe humano
    print("\n🧬 INFORME DE IMPACTO\n")

    for d in diffs:
        print(f"\n📄 Archivo: {d['file']}")
        print(f"Tipo de cambio: {d['type']}")

        if d["diff"]:
            print("\n".join(d["diff"]))
        else:
            print("Archivo nuevo.")