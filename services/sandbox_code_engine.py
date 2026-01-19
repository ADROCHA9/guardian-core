# services/sandbox_code_engine.py
from execution.sandbox_manager import SandboxManager
from execution.code_generator import generate_code_suggestion


def prepare_code_evolution(memory, proposal):
    """
    Genera código en sandbox basado en una propuesta.
    """
    sandbox = SandboxManager(memory.get("project")["root_path"])
    sandbox_path = sandbox.create()

    code = generate_code_suggestion(
        proposal=proposal,
        context=memory._memory
    )

    return {
        "sandbox_path": sandbox_path,
        "generated_code": code,
        "proposal": proposal
    }