from __future__ import annotations

import secrets

from passlib.context import CryptContext


# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(
    password: str,
) -> str:
    """
    Hash a plaintext password.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password
    against its hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# Secure Tokens
# ==========================================================

def generate_secret_token(
    length: int = 32,
) -> str:
    """
    Generate a cryptographically
    secure random token.
    """

    return secrets.token_urlsafe(
        length
    )


def generate_order_reference() -> str:
    """
    Generate a unique order reference.
    """

    return secrets.token_hex(
        8
    ).upper()