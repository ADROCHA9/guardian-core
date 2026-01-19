# security/authentication/password_guard.py
import hashlib
import hmac


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña.
    """
    if not isinstance(password, str) or not password:
        raise ValueError("Contraseña inválida")

    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verifica una contraseña contra su hash almacenado.
    """
    if not password or not stored_hash:
        return False

    computed = hash_password(password)
    return hmac.compare_digest(computed, stored_hash)