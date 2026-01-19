from datetime import datetime


class HumanHelpExclusionTask:
    """
    Define dominios donde Guardian no debe pedir ayuda humana.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.setdefault("cognitive_memory", {})
        guardian = self.memory._memory.setdefault("guardian_self", {})

        metrics = cognitive.get("metrics", {}).get("daily", {})
        patterns = cognitive.get("error_patterns", [])

        if len(metrics) < 7:
            return None

        last_week = list(metrics.values())[-7:]
        avg_progress = sum(
            d.get("concepts_used", 0) for d in last_week
        ) / len(last_week)

        if avg_progress >= 2 and not any(
            p.get("active") for p in patterns
        ):
            excluded = guardian.setdefault("no_help_domains", [])

            domain = guardian.get("learning_intent", {}).get("goal")
            if domain and domain not in excluded:
                excluded.append(domain)

                self.memory.log_event(
                    event="human_help_excluded",
                    summary=f"Guardian no pedirá ayuda humana en dominio: {domain}"
                )
                self.memory._persist()

                return domain

        return None