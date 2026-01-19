# intelligence/ai_consultant.py
from typing import Dict


class AIConsultant:
    """
    Consultor soberano. Nunca ejecuta.
    """

    def __init__(self, client, name: str):
        self.client = client
        self.name = name

    def consult(self, prompt: str) -> Dict[str, str]:
        response = self.client.generate(prompt)
        return {
            "provider": self.name,
            "raw_response": response
        }