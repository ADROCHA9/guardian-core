import ast
from typing import Dict, List, Set


# --------------------------------------------------
# 1️⃣ VALIDACIÓN DE SINTAXIS
# --------------------------------------------------
def validate_syntax(files: Dict[str, dict]) -> List[Dict]:
    issues = []

    for path, data in files.items():
        try:
            source = data.get("_source")
            if source:
                ast.parse(source)
        except SyntaxError as e:
            issues.append({
                "level": "high",
                "file": path,
                "type": "syntax_error",
                "description": f"Error de sintaxis: {e.msg}",
                "suggestion": "corregir sintaxis antes de continuar"
            })

    return issues


# --------------------------------------------------
# 2️⃣ DETECCIÓN DE BUGS ESTÁTICOS
# --------------------------------------------------
def detect_static_bugs(files: Dict[str, dict]) -> List[Dict]:
    issues = []

    for path, data in files.items():
        structure = data.get("structure", {})
        functions = set(structure.get("functions", []))
        classes = set(structure.get("classes", []))
        imports = set(structure.get("imports", []))

        # funciones definidas pero no usadas (heurística)
        if functions and not data.get("relations", {}).get("used_by"):
            issues.append({
                "level": "low",
                "file": path,
                "type": "unused_definitions",
                "description": "funciones o clases definidas pero no utilizadas",
                "suggestion": "verificar si son necesarias o faltan conexiones"
            })

        # imports sin uso (heurística simple)
        if imports and not functions and not classes:
            issues.append({
                "level": "low",
                "file": path,
                "type": "unused_imports",
                "description": "imports detectados sin uso evidente",
                "suggestion": "limpiar o justificar imports"
            })

    return issues


# --------------------------------------------------
# 3️⃣ COHERENCIA CONCEPTUAL
# --------------------------------------------------
def check_conceptual_coherence(
    project_purpose: str,
    files: Dict[str, dict]
) -> List[Dict]:
    issues = []

    purpose = project_purpose.lower()

    for path, data in files.items():
        role = data.get("role", "").lower()
        intent = data.get("intent", {}).get("what_it_does", "").lower()

        if purpose and role and purpose not in role and purpose not in intent:
            issues.append({
                "level": "medium",
                "file": path,
                "type": "conceptual_drift",
                "description": "el módulo no encaja claramente en el propósito del sistema",
                "suggestion": "definir explícitamente su rol o reconsiderar su inclusión"
            })

    return issues


# --------------------------------------------------
# 4️⃣ CONTINUIDAD HISTÓRICA
# --------------------------------------------------
def check_historical_continuity(
    files: Dict[str, dict],
    evolution_log: List[dict]
) -> List[Dict]:
    issues = []

    previously_known: Set[str] = set()
    for event in evolution_log:
        if event["event"] == "file_registered":
            previously_known.add(event["summary"].split(": ")[-1])

    current_files = set(files.keys())

    # Archivos nuevos sin contexto histórico
    new_files = current_files - previously_known
    for f in new_files:
        issues.append({
            "level": "medium",
            "file": f,
            "type": "new_module_uncontextualized",
            "description": "nuevo módulo detectado sin justificación histórica",
            "suggestion": "explicar por qué se incorpora y qué problema resuelve"
        })

    # Archivos desaparecidos
    removed_files = previously_known - current_files
    for f in removed_files:
        issues.append({
            "level": "high",
            "file": f,
            "type": "module_removed",
            "description": "módulo previamente existente ya no está presente",
            "suggestion": "confirmar eliminación o restaurar coherencia"
        })

    return issues


# --------------------------------------------------
# 🧠 ORQUESTADOR GENERAL
# --------------------------------------------------
def validate_system(memory_snapshot: Dict) -> List[Dict]:
    issues = []

    project = memory_snapshot.get("project", {})
    files = memory_snapshot.get("files", {})
    evolution_log = memory_snapshot.get("evolution_log", [])

    issues.extend(validate_syntax(files))
    issues.extend(detect_static_bugs(files))
    issues.extend(check_conceptual_coherence(
        project.get("purpose", ""),
        files
    ))
    issues.extend(check_historical_continuity(
        files,
        evolution_log
    ))

    return issues