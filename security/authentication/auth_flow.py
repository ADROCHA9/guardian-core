# security/authentication/auth_flow.py
def authenticate(*args, **kwargs):
    raise RuntimeError(
        "auth_flow está deshabilitado. "
        "Usar identity_manager.ensure_identity."
    )