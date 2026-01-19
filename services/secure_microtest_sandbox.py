import builtins
import threading


class SecureMicroTestSandbox:
    """
    Sandbox endurecido para micro-tests.
    Bloquea:
    - imports peligrosos
    - acceso a filesystem
    - eval / exec externos
    """

    ALLOWED_BUILTINS = {
        "range", "len", "print", "int", "float",
        "str", "bool", "list", "dict", "set",
        "tuple", "enumerate", "sum", "min", "max"
    }

    def __init__(self):
        self.safe_builtins = {
            k: getattr(builtins, k)
            for k in self.ALLOWED_BUILTINS
            if hasattr(builtins, k)
        }

    def execute(self, code: str, expect: str):
        local_env = {}

        globals_env = {
            "__builtins__": self.safe_builtins
        }

        exec(code, globals_env, local_env)
        return local_env.get(expect)