import hashlib
import json
from datetime import datetime


class KnowledgeSignatureTask:
    """
    Firma criptográficamente el conocimiento cognitivo.
    """

    def __init__(self, memory):
        self.memory = memory

    def sign(self):
        cognitive = self.memory._memory.get("cognitive_memory", {})

        payload = json.dumps(
            cognitive,
            sort_keys=True,
            ensure_ascii=False
        ).encode("utf-8")

        signature = hashlib.sha256(payload).hexdigest()

        self.memory._memory.setdefault("guardian_self", {})[
            "knowledge_signature"
        ] = {
            "hash": signature,
            "signed_at": datetime.utcnow().isoformat()
        }

        self.memory.log_event(
            event="knowledge_signed",
            summary="Conocimiento cognitivo firmado criptográficamente"
        )
        self.memory._persist()

        return signature