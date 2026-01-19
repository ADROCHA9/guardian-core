class OperatorCommunicationFilterTask:
    """
    Decide cuándo Guardian debe comunicar al operador.
    """

    def __init__(self, memory):
        self.memory = memory

    def run(self, message, importance="low"):
        if importance == "low":
            return None  # callar

        self.memory._memory.setdefault("guardian_self", {}).setdefault(
            "operator_messages", []
        ).append(message)

        self.memory._persist()
        return message