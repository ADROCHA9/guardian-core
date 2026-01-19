# security/root_protection/root_resolver.py
import os

def resolve_guardian_root() -> str:
    """
    Resuelve la raíz real del Guardian dinámicamente.
    """
    here = os.path.abspath(__file__)
    # security/root_protection/ -> subir 3 niveles
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    return os.path.abspath(root)