"""Security primitives shared by authentication and user management."""

from pwdlib import PasswordHash

_password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return an Argon2 password hash; never persist the plain-text password."""
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Validate a plain-text password against its stored Argon2 hash."""
    return _password_hasher.verify(password, password_hash)
