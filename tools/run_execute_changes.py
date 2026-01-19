# tools/run_execute_changes.py
from memory import ProjectMemory
from execution.sandbox_manager import SandboxManager
from execution.ai_analysis_flow import run_ai_analysis
from execution.ai_to_code_generator import apply_ai_suggestions_to_sandbox
from execution.test_runner import TestRunner
from execution.diff_engine import DiffEngine
from execution.confirmation import request_confirmation
from execution.authorization import AuthorizationManager
from execution.execution_guard import ExecutionGuard
from execution.applier import Applier
from execution.evolution_log import EvolutionLog


if __name__ == "__main__":
    ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"

    # 1️⃣ Cargar memoria
    memory = ProjectMemory(ROOT)
    memory.load()

    # 2️⃣ Guard de ejecución
    guard = ExecutionGuard(memory._memory)
    if not guard.can_execute():
        print("🚫 Nivel de ejecución insuficiente.")
        exit(1)

    # 3️⃣ Autorización por clave
    auth = AuthorizationManager(memory._memory)
    if not auth.validate():
        exit(1)

    # 4️⃣ Sandbox
    sandbox = SandboxManager(ROOT)
    sandbox_path = sandbox.create()

    # 5️⃣ Análisis IA
    analysis = run_ai_analysis(
        task="Proponer mejoras estructurales para el Guardian",
        memory_snapshot=memory._memory
    )

    if not analysis:
        print("❌ No se obtuvo análisis IA.")
        exit(1)

    # 6️⃣ Aplicar sugerencias IA en sandbox
    target_files = ["proposal_engine.py"]
    changes = apply_ai_suggestions_to_sandbox(
        analysis_text=analysis,
        sandbox_path=sandbox_path,
        target_files=target_files
    )

    if not changes:
        print("⚠️ No se generaron cambios.")
        exit(0)

    # 7️⃣ Tests
    runner = TestRunner(sandbox_path)
    results = runner.run_basic_tests(
        files=[c["file"] for c in changes]
    )

    if any(r["status"] != "ok" for r in results):
        print("❌ Tests fallidos. Ejecución bloqueada.")
        exit(1)

    # 8️⃣ Diff
    diff_engine = DiffEngine(ROOT, sandbox_path)
    diffs = diff_engine.run([c["file"] for c in changes])

    print("\n🧬 CAMBIOS PROPUESTOS\n")
    for d in diffs:
        print(f"\nArchivo: {d['file']}")
        if d["diff"]:
            print("\n".join(d["diff"]))

    # 9️⃣ Confirmación humana
    if not request_confirmation("¿Desea aplicar estos cambios al proyecto real?"):
        print("❎ Cambios cancelados por el usuario.")
        exit(0)

    # 🔟 Aplicar cambios reales
    applier = Applier(ROOT, sandbox_path)
    applier.apply_files([c["file"] for c in changes])

    # 1️⃣1️⃣ Registrar evolución
    evo = EvolutionLog(memory._memory)
    evo.record(
        proposal_id="ia_generated_change",
        action="apply",
        result="success",
        details={"files": [c["file"] for c in changes]}
    )

    memory.update_project_scan_time()
    print("\n✅ CAMBIOS APLICADOS CORRECTAMENTE.")