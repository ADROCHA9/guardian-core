import os

from memory import ProjectMemory
from scanner import scan_tree
from parser import parse_python_file
from relationer import build_relations
from validator import validate_system
from question_engine import generate_questions
from watchdog import scan_changes
from narrator import narrate_system
from proposal_engine import generate_proposals

from environment.environment_state import collect_environment_state


def run(root_path: str) -> None:
    print("🧠 Guardian Bot iniciado")
    print(f"📁 Root soberano: {root_path}")

    # =====================================================
    # 1️⃣ Cargar memoria persistente
    # =====================================================
    memory = ProjectMemory(root_path)
    memory.load()

    # =====================================================
    # 1.5️⃣ Conciencia del entorno (HARDWARE / OS / MODO)
    # =====================================================
    env_state = collect_environment_state()
    memory.set_environment(env_state)

    memory.log_event(
        event="environment_detected",
        summary=f"Modo: {env_state['mode']['mode']}"
    )

    # =====================================================
    # 2️⃣ Escaneo informativo del proyecto
    # =====================================================
    files = scan_tree(root_path)
    print(f"🔍 Archivos detectados: {len(files)}")

    # =====================================================
    # 3️⃣ Detección de cambios (watchdog)
    # =====================================================
    changes = scan_changes(root_path, memory.get("files"))

    if any(changes.values()):
        memory.log_event(
            event="filesystem_change",
            summary=(
                f"Nuevos: {len(changes['new_files'])}, "
                f"Modificados: {len(changes['modified_files'])}, "
                f"Eliminados: {len(changes['removed_files'])}"
            )
        )

    # =====================================================
    # 4️⃣ Análisis incremental
    # =====================================================
    files_to_process = set(changes["new_files"]) | set(changes["modified_files"])

    for relative_path in files_to_process:
        absolute_path = os.path.join(root_path, relative_path)
        print(f"📄 Analizando: {relative_path}")

        try:
            parsed_data = parse_python_file(absolute_path, relative_path)
            memory.register_file(relative_path, parsed_data)

            memory.log_event(
                event="file_analyzed",
                summary=f"Archivo analizado: {relative_path}"
            )

        except Exception as e:
            memory.add_inconsistency({
                "level": "high",
                "file": relative_path,
                "type": "parse_error",
                "description": str(e),
                "suggestion": "revisar sintaxis o codificación"
            })

    # =====================================================
    # 5️⃣ Archivos eliminados
    # =====================================================
    for removed in changes["removed_files"]:
        memory.add_inconsistency({
            "level": "high",
            "file": removed,
            "type": "file_removed",
            "description": "archivo eliminado del proyecto",
            "suggestion": "confirmar si la eliminación es intencional"
        })

    # =====================================================
    # 6️⃣ Relaciones sistémicas
    # =====================================================
    relations = build_relations(memory.get("files"))
    for r in relations:
        memory.add_relation(r)

    memory.log_event(
        event="relations_built",
        summary=f"{len(relations)} relaciones detectadas"
    )

    # =====================================================
    # 7️⃣ Validación de coherencia
    # =====================================================
    issues = validate_system(memory._memory)
    for issue in issues:
        memory.add_inconsistency(issue)

    memory.log_event(
        event="validation_complete",
        summary=f"{len(issues)} inconsistencias detectadas"
    )

    # =====================================================
    # 8️⃣ Preguntas conscientes
    # =====================================================
    questions = generate_questions(memory._memory)
    for q in questions:
        memory.add_question(q)

    if questions:
        memory.log_event(
            event="questions_generated",
            summary=f"{len(questions)} preguntas abiertas"
        )

    # =====================================================
    # 9️⃣ Narrativa del sistema
    # =====================================================
    narration = narrate_system(memory._memory)

    for section, text in narration.items():
        print(f"\n🧭 {section.upper()}")
        print(text)

    # =====================================================
    # 🔟 Propuestas del sistema
    # =====================================================
    proposals = generate_proposals(memory._memory)

    for p in proposals:
        memory.add_proposed_connection(p)

    if proposals:
        memory.log_event(
            event="system_proposals_generated",
            summary=f"{len(proposals)} propuestas generadas"
        )

        print("\n💡 PROPUESTAS DEL SISTEMA")
        for p in proposals:
            print(f"- ({p['priority'].upper()}) {p['description']}")

    # =====================================================
    # 1️⃣1️⃣ Cierre del ciclo
    # =====================================================
    memory.update_project_scan_time()
    memory.log_event(
        event="guardian_cycle_complete",
        summary="Ciclo de análisis y conciencia completado"
    )

    print("\n✅ Guardian estable. Conciencia sincronizada.")


if __name__ == "__main__":
    ROOT = "C:/Users/CONECTIA BA/OneDrive/Escritorio/NICONO v3.0"
    run(ROOT)