import os
from typing import List

ALLOWED_EXTENSIONS = (".py",)


def scan_tree(root_path: str) -> List[str]:
    files = []

    for root, _, filenames in os.walk(root_path):
        # ignorar carpetas internas del bot
        if "guardian_bot" in root:
            continue

        for name in filenames:
            if name.endswith(ALLOWED_EXTENSIONS):
                full_path = os.path.join(root, name)
                normalized = os.path.relpath(full_path, root_path)
                files.append(normalized.replace("\\", "/"))

    return files