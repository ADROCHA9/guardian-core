# services/self_analysis_engine.py

def analyze_self(memory):
    guardian_files = {
        k: v for k, v in (memory.get("files") or {}).items()
        if "guardian" in k or "services" in k or "gui" in k
    }

    findings = []

    for path, data in guardian_files.items():
        functions = data.get("structure", {}).get("functions", [])
        if len(functions) > 15:
            findings.append({
                "type": "self_complexity",
                "file": path,
                "description": "Archivo con alta complejidad funcional",
                "suggestion": "Dividir responsabilidades"
            })

    return findings