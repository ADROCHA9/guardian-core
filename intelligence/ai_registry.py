import subprocess
from typing import Dict, List


def detect_ollama() -> Dict:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return {"available": False}

        models = []
        for line in result.stdout.splitlines()[1:]:
            if line.strip():
                models.append(line.split()[0])

        return {
            "available": True,
            "provider": "ollama",
            "models": models
        }

    except Exception:
        return {"available": False}


def detect_ai_providers() -> List[Dict]:
    providers = []
    ollama = detect_ollama()
    if ollama.get("available"):
        providers.append(ollama)
    return providers