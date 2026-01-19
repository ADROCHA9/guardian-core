from typing import Dict, List
from collections import defaultdict


def build_relations(files_data: Dict[str, dict]) -> List[dict]:
    relations = []
    usage_counter = defaultdict(int)

    # Normalizar nombres de módulo → archivo
    module_to_file = {}
    for path in files_data:
        module_name = path.replace("/", ".").replace(".py", "")
        module_to_file[module_name] = path

    # Analizar dependencias
    for file_path, data in files_data.items():
        imports = data.get("structure", {}).get("imports", [])

        for imp in imports:
            for module, target_file in module_to_file.items():
                if imp in module:
                    relations.append({
                        "type": "dependency",
                        "from": file_path,
                        "to": target_file,
                        "status": "detected"
                    })
                    usage_counter[target_file] += 1

    # Detectar módulos huérfanos
    for file_path in files_data:
        if usage_counter[file_path] == 0:
            relations.append({
                "type": "orphan_module",
                "file": file_path,
                "description": "módulo no utilizado por otros"
            })

    # Detectar núcleos centrales
    for file_path, count in usage_counter.items():
        if count >= 3:
            relations.append({
                "type": "central_module",
                "file": file_path,
                "usage_count": count,
                "description": "módulo con alta dependencia"
            })

    return relations