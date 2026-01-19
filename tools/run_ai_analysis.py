# tools/run_ai_analysis.py
from memory import ProjectMemory
from execution.ai_analysis_flow import run_ai_analysis


if __name__ == "__main__":
    ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"

    memory = ProjectMemory(ROOT)
    memory.load()

    analysis = run_ai_analysis(
        task="Proponer mejoras estructurales para el Guardian",
        memory_snapshot=memory._memory
    )

    if analysis:
        print("\n🧠 ANÁLISIS IA\n")
        print(analysis)