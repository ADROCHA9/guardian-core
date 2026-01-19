import subprocess
from typing import Optional


class OllamaClient:
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            process = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=120
            )

            if process.returncode != 0:
                raise RuntimeError(process.stderr)

            return process.stdout.strip()

        except subprocess.TimeoutExpired:
            raise RuntimeError("Timeout consultando Ollama")