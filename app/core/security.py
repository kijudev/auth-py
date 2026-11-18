import secrets
from typing import NewType

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from blake3 import blake3

# >--------------------------------------------------------- Types and Constants

Token = NewType("Token", str)
TokenHash = NewType("TokenHash", str)

password_hasher = PasswordHasher()
DUMMY_PASSWORD_HASH = password_hasher.hash("dummy-password")

# >----------------------------------------------------------------------- Utils


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerificationError, InvalidHashError:
        return False


def generate_session_token() -> Token:
    return Token(secrets.token_urlsafe(32))


def hash_session_token(token: Token) -> TokenHash:
    return TokenHash(blake3(token.encode()).hexdigest())
