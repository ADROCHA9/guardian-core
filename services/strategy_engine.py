from collections import defaultdict, deque


class StrategyEngine:
    """
    Motor estratégico del Guardian.
    No ejecuta cambios. Solo analiza, ordena y simula.
    """

    def __init__(self, memory):
        self.memory = memory

    # =================================================
    # CONFLICTOS
    # =================================================
    def detect_conflicts(self):
        proposals = self.memory.get("proposed_connections", [])
        conflicts = []

        for i, a in enumerate(proposals):
            for b in proposals[i + 1:]:
                # Conflicto simple: mismo tipo + misma prioridad
                if (
                    a.get("type") == b.get("type")
                    and a.get("priority") is not None
                    and a.get("priority") == b.get("priority")
                ):
                    conflicts.append({
                        "a": a["id"],
                        "b": b["id"],
                        "reason": "Mismo tipo y misma prioridad"
                    })

        return conflicts

    def suggest_conflict_resolution(self, conflict):
        return (
            f"Conflicto entre {conflict['a']} y {conflict['b']}.\n"
            "Sugerencias:\n"
            "- Cambiar prioridad de una propuesta\n"
            "- Definir dependencia explícita\n"
            "- Rechazar una de las propuestas"
        )

    # =================================================
    # PLANIFICADOR POR PRIORIDADES
    # =================================================
    def plan_by_priority(self):
        proposals = self.memory.get("proposed_connections", [])

        # Grafo de dependencias
        graph = defaultdict(list)
        indegree = defaultdict(int)

        nodes = {p["id"]: p for p in proposals}

        for p in proposals:
            pid = p["id"]
            deps = p.get("depends_on", [])
            for d in deps:
                graph[d].append(pid)
                indegree[pid] += 1

            indegree.setdefault(pid, 0)

        # Orden topológico (dependencias)
        queue = deque(
            pid for pid, deg in indegree.items() if deg == 0
        )

        ordered = []

        while queue:
            pid = queue.popleft()
            ordered.append(nodes[pid])

            for nxt in graph[pid]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

        # Ordenar por prioridad dentro del orden válido
        ordered.sort(
            key=lambda p: p.get("priority") if p.get("priority") is not None else 999
        )

        return ordered

    # =================================================
    # SIMULACIÓN DE ROADMAP
    # =================================================
    def simulate_roadmap(self):
        plan = self.plan_by_priority()

        roadmap = []
        step = 1

        for p in plan:
            roadmap.append({
                "step": step,
                "proposal_id": p["id"],
                "description": p.get("description"),
                "priority": p.get("priority"),
                "type": p.get("type")
            })
            step += 1

        return roadmap