from __future__ import annotations

from typing import Any, Dict


class SecurityHelpers:
    """Utility helpers for auth and token handling."""

    @staticmethod
    def hash_password(password: str) -> str:
        # Real implementation should use passlib or bcrypt
        return f"hashed::{password}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return password_hash == f"hashed::{password}"

    @staticmethod
    def create_token(sub: str) -> Dict[str, str]:
        return {"sub": sub, "token_type": "bearer"}


__all__ = ["SecurityHelpers"]
