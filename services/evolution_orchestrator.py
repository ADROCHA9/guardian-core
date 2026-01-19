from services.sandbox_code_engine import prepare_code_evolution


def evolve(memory):
    """
    Prepara evolución SOLO para propuestas humanas o aprobadas.
    NO ejecuta nada.
    """

    proposals = memory.get("proposed_connections") or []
    prepared = []

    for proposal in proposals:
        if proposal.get("status") == "new" and proposal.get("origin") == "human":
            evo = prepare_code_evolution(memory, proposal)

            proposal["status"] = "prepared"
            proposal["sandbox"] = evo

            prepared.append(proposal)

    if prepared:
        memory.log_event(
            event="evolution_prepared",
            summary=f"{len(prepared)} evoluciones listas para sandbox"
        )

        memory._persist()