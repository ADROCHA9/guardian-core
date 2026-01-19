import os
import hashlib
from typing import Dict


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_changes(root_path: str, memory_files: Dict[str, dict]) -> Dict[str, list]:
    """
    Devuelve:
      - new_files
      - modified_files
      - removed_files
    """
    current_files = {}
    for root, _, files in os.walk(root_path):
        if "guardian_bot" in root:
            continue
        for name in files:
            if name.endswith(".py"):
                abs_path = os.path.join(root, name)
                rel = os.path.relpath(abs_path, root_path).replace("\\", "/")
                current_files[rel] = file_hash(abs_path)

    known_files = set(memory_files.keys())
    current_set = set(current_files.keys())

    new_files = list(current_set - known_files)
    removed_files = list(known_files - current_set)

    modified_files = []
    for f in current_set & known_files:
        prev_hash = memory_files[f].get("_hash")
        if prev_hash and prev_hash != current_files[f]:
            modified_files.append(f)

    return {
        "new_files": new_files,
        "modified_files": modified_files,
        "removed_files": removed_files,
        "current_hashes": current_files
    }