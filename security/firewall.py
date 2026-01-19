# security/firewall.py
FORBIDDEN_PATTERNS = [
    "os.system",
    "subprocess",
    "rm -rf",
    "del /",
    "eval(",
    "exec(",
    "open(",
    "__import__",
    "socket",
    "requests"
]


def scan_text(text: str) -> None:
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in text:
            raise ValueError(
                f"Respuesta bloqueada por firewall (patrón: {pattern})"
            )