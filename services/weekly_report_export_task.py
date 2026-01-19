import os
from datetime import datetime, timedelta
import json


class WeeklyReportExportTask:
    """
    Genera reportes semanales automáticos del estado cognitivo.
    No bloquea, no consume CPU, corre 1 vez por semana.
    """

    def __init__(self, memory, reports_dir="reports"):
        self.memory = memory
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def should_run(self) -> bool:
        guardian = self.memory._memory.setdefault("guardian_self", {})
        last = guardian.get("last_weekly_report")

        if not last:
            return True

        try:
            last_dt = datetime.fromisoformat(last)
        except Exception:
            return True

        return datetime.utcnow() - last_dt >= timedelta(days=7)

    def run(self):
        if not self.should_run():
            return None

        cognitive = self.memory._memory.get("cognitive_memory", {})
        metrics = cognitive.get("metrics", {})
        heuristics = cognitive.get("error_heuristics", [])
        patterns = cognitive.get("error_patterns", [])
        plans = cognitive.get("proposed_plans", [])

        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "metrics": metrics,
            "active_heuristics": [
                h for h in heuristics if h.get("active", True)
            ],
            "error_patterns": patterns,
            "proposed_plans": plans[-5:]
        }

        filename = f"weekly_report_{datetime.utcnow().date().isoformat()}.json"
        path = os.path.join(self.reports_dir, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.memory._memory.setdefault("guardian_self", {})[
            "last_weekly_report"
        ] = datetime.utcnow().isoformat()

        self.memory.log_event(
            event="weekly_report_exported",
            summary=f"Reporte semanal exportado: {filename}"
        )
        self.memory._persist()

        return path