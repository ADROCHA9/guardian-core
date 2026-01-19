from execution.ai_consultation_step import run_ai_consultation

text = run_ai_consultation(
    task="Proponer mejoras estructurales para el Guardian",
    memory_snapshot=memory._memory
)

if text:
    print(text)