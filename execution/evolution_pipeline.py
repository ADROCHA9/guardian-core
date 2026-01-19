# execution/evolution_pipeline.py
from execution.applier import apply_changes
from execution.authorization import authorize_execution


def apply_evolution(memory, proposal, password):
    """
    Aplica una evolución ya preparada, con autorización humana.
    """
    if not authorize_execution(memory, password):
        raise PermissionError("Autorización inválida")

    sandbox = proposal["sandbox"]

    result = apply_changes(
        sandbox_path=sandbox["sandbox_path"],
        project_root=memory.get("project")["root_path"],
        changes=sandbox["generated_code"],
        memory=memory
    )

    proposal["status"] = "applied"
    return result