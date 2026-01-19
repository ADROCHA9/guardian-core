# intelligence/knowledge_bridge.py
from typing import List


def extract_code_blocks(text: str) -> List[str]:
    """
    Extrae bloques de código delimitados por ``` del texto.
    """
    blocks = []
    current = []
    in_block = False

    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_block = not in_block
            if not in_block and current:
                blocks.append("\n".join(current))
                current = []
            continue

        if in_block:
            current.append(line)

    return blocks