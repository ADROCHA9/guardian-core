from datetime import datetime


class HumanInterventionComparisonTask:
    """
    Compara la efectividad de distintos tipos de intervención humana.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        styles = cognitive.get("human_help_styles", {})

        if not styles:
            return None

        comparison = []

        for style, stats in styles.items():
            total = sum(stats.values())
            success_rate = (
                stats["successful"] / total if total > 0 else 0
            )

            comparison.append({
                "style": style,
                "success_rate": round(success_rate, 2),
                "total_uses": total
            })

        comparison.sort(key=lambda x: x["success_rate"], reverse=True)

        cognitive["human_intervention_comparison"] = {
            "generated_at": datetime.utcnow().isoformat(),
            "ranking": comparison
        }

        self.memory.log_event(
            event="human_interventions_compared",
            summary="Comparación de intervenciones humanas actualizada"
        )
        self.memory._persist()

        return comparison