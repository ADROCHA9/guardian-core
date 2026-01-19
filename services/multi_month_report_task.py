from datetime import datetime
import json
import os


class MultiMonthReportTask:
    """
    Genera reportes comparativos entre meses.
    """

    def __init__(self, memory, reports_dir="reports"):
        self.memory = memory
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def run(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {}).get("daily", {})

        if not metrics:
            return None

        monthly = {}
        for day, data in metrics.items():
            month = day[:7]  # YYYY-MM
            monthly.setdefault(month, 0)
            monthly[month] += data.get("concepts_used", 0)

        months = sorted(monthly.keys())
        comparisons = []

        for i in range(1, len(months)):
            prev, curr = months[i - 1], months[i]
            delta = monthly[curr] - monthly[prev]

            comparisons.append({
                "from": prev,
                "to": curr,
                "delta": delta,
                "trend": (
                    "improving" if delta > 0 else
                    "declining" if delta < 0 else
                    "stable"
                )
            })

        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "monthly_totals": monthly,
            "comparisons": comparisons
        }

        path = os.path.join(
            self.reports_dir,
            f"multi_month_report_{datetime.utcnow().date().isoformat()}.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.memory.log_event(
            event="multi_month_report_generated",
            summary="Reporte comparativo multi-mes generado"
        )
        self.memory._persist()

        return path