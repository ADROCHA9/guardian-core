# tools/run_ai_to_sandbox.py
from memory import ProjectMemory
from execution.sandbox_manager import SandboxManager
from execution.ai_analysis_flow import run_ai_analysis
from execution.ai_to_code_generator import apply_ai_suggestions_to_sandbox


if __name__ == "__main__":
    ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"

    memory = ProjectMemory(ROOT)
    memory.load()

    sandbox = SandboxManager(ROOT)
    sandbox_path = sandbox.create()

    analysis = run_ai_analysis(
        task="Proponer mejoras estructurales para el Guardian",
        memory_snapshot=memory._memory
    )

    if analysis:
        changes = apply_ai_suggestions_to_sandbox(
            analysis_text=analysis,
            sandbox_path=sandbox_path,
            target_files=["proposal_engine.py"]
        )

        print("\n🧪 CAMBIOS EN SANDBOX\n")
        for c in changes:
            print(c)