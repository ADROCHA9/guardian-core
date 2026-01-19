# execution/confirmation.py
def request_confirmation(summary: str) -> bool:
    print("\n🔐 CONFIRMACIÓN REQUERIDA")
    print(summary)
    answer = input("\n¿Desea aplicar estos cambios al proyecto real? (s/n): ")
    return answer.strip().lower() in ("s", "si", "y", "yes")
