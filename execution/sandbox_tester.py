# execution/sandbox_tester.py
import tempfile
import os
import importlib.util


def test_code_in_sandbox(code: str) -> bool:
    """
    Ejecuta import del código en sandbox temporal.
    """
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test_module.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        spec = importlib.util.spec_from_file_location("test_module", path)
        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise ValueError(f"Fallo en sandbox: {e}")

    return True