def format_sandbox_report(report: dict) -> str:
    """
    Convierte un reporte de sandbox en texto humano.
    """
    if report["status"] != "success":
        return (
            "❌ La simulación falló.\n"
            f"Error:\n{report.get('errors')}"
        )

    effects = report.get("effects", {})

    lines = [
        "🧪 Resultado del Sandbox:",
        f"- Archivos nuevos: {effects.get('files_delta', 0)}",
        f"- Cambios de relaciones: {effects.get('relations_delta', 0)}",
        f"- Inconsistencias: {effects.get('inconsistencies_delta', 0)}",
    ]

    notes = effects.get("notes", [])
    if notes:
        lines.append("Notas:")
        for n in notes:
            lines.append(f"• {n}")

    lines.append("\n¿Confirmás aplicar esta evolución?")
    return "\n".join(lines)