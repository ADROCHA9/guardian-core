# services/communication_bridge.py

from services.guardian_cognitive_core import GuardianCognitiveCore


class CommunicationBridge:
    """
    Puente nervioso principal Humano ↔ Guardian.
    TODA comunicación pasa por el cerebro cognitivo.
    """

    def __init__(self, memory, on_response):
        self.memory = memory
        self.on_response = on_response
        self.brain = GuardianCognitiveCore(memory)

    # =================================================
    # ENTRADA HUMANA
    # =================================================
    def receive(self, text: str):
        """
        Entrada directa del humano al sistema nervioso.
        """
        result = self.brain.think(human_input=text)
        self._emit(result)

    # =================================================
    # SALIDA DEL GUARDIAN
    # =================================================
    def _emit(self, result: dict):
        """
        Emite respuesta unificada del Guardian.
        """
        response = result.get("response", "")

        if result.get("questions"):
            response += "\n\n❓ Preguntas para avanzar:\n"
            for q in result["questions"]:
                response += f"- {q.get('question')}\n"

        if result.get("suggestions"):
            response += "\n\n💡 Sugerencias del Guardian:\n"
            for s in result["suggestions"]:
                desc = s.get("description") or s.get("type", "")
                response += f"- {desc}\n"

        self.on_response(response)