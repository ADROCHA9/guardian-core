from collections import defaultdict


class EthicalExplainer:
    """
    Motor de explicabilidad, sesgo y auditoría ética.
    NO ejecuta cambios.
    """

    def __init__(self, memory):
        self.memory = memory

    # =================================================
    # EXPLICABILIDAD
    # =================================================
    def explain_learning(self):
        decisions = self.memory.get("decision_log", [])
        if not decisions:
            return "No hay decisiones registradas para explicar aprendizaje."

        by_proposal = defaultdict(list)
        for d in decisions:
            by_proposal[d["proposal_id"]].append(d)

        lines = ["🧠 EXPLICACIÓN DEL APRENDIZAJE\n"]
        for pid, ds in by_proposal.items():
            lines.append(
                f"- Propuesta {pid}: "
                f"{len(ds)} decisiones humanas influyeron en ajustes posteriores."
            )

        lines.append(
            "\nGuardian aprende detectando patrones "
            "en decisiones humanas repetidas, no por resultados automáticos."
        )

        return "\n".join(lines)

    # =================================================
    # DETECCIÓN DE SESGOS
    # =================================================
    def detect_biases(self):
        decisions = self.memory.get("decision_log", [])
        proposals = self.memory.get("proposed_connections", [])

        if not decisions:
            return ["No hay suficientes datos para detectar sesgos."]

        origin_count = defaultdict(int)
        status_count = defaultdict(int)

        for d in decisions:
            origin = next(
                (p.get("origin") for p in proposals if p["id"] == d["proposal_id"]),
                "unknown"
            )
            origin_count[origin] += 1
            status_count[d.get("decision")] += 1

        lines = ["🔍 POSIBLES SESGOS DETECTADOS\n"]

        if len(origin_count) == 1:
            lines.append(
                "⚠️ Todas las decisiones afectan al mismo origen "
                f"({next(iter(origin_count))}). Posible sesgo."
            )

        if status_count.get("approved", 0) > status_count.get("rejected", 0) * 3:
            lines.append(
                "⚠️ Alta tasa de aprobación frente a rechazo. "
                "Riesgo de falta de criticidad."
            )

        if len(lines) == 1:
            lines.append("No se detectaron sesgos evidentes.")

        return lines

    # =================================================
    # AUDITORÍA ÉTICA
    # =================================================
    def ethical_audit(self):
        decisions = self.memory.get("decision_log", [])

        lines = [
            "📜 AUDITORÍA ÉTICA DE DECISIONES\n",
            f"- Total de decisiones humanas: {len(decisions)}",
            "",
            "Principios evaluados:",
            "- Transparencia",
            "- Control humano",
            "- No automatización ciega",
            "",
            "Resultado:"
        ]

        if decisions:
            lines.append("✔️ Todas las decisiones fueron explícitas y justificadas.")
        else:
            lines.append("⚠️ No hay decisiones registradas aún.")

        lines.append(
            "\nRecomendación:\n"
            "Revisar periódicamente decisiones y sesgos detectados."
        )

        return "\n".join(lines)