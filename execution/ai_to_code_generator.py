# execution/ai_to_code_generator.py
from typing import Dict, List

from intelligence.knowledge_bridge import extract_code_blocks
from execution.code_generator import CodeGenerator


def apply_ai_suggestions_to_sandbox(
    analysis_text: str,
    sandbox_path: str,
    target_files: List[str]
) -> List[Dict]:
    """
    Toma texto de IA, extrae bloques de código
    y los aplica en sandbox usando CodeGenerator.
    """

    generator = CodeGenerator(sandbox_path)
    code_blocks = extract_code_blocks(analysis_text)

    if not code_blocks:
        return []

    for i, block in enumerate(code_blocks):
        # Estrategia simple inicial:
        # cada bloque corresponde a un archivo target
        if i < len(target_files):
            generator.modify_file(
                relative_path=target_files[i],
                new_content=block
            )

    return generator.get_changes()