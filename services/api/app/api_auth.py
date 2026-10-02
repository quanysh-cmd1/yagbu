from __future__ import annotations

from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status

from .core.config import settings
from .queues import JobQueue


class ApiKeyAuth:
    """Very small API key auth stub."""

    def __init__(self):
        self.valid_keys = {"test_key_demo": {"org_id": "org-default", "user_id": "user-default"}}

    def authenticate(self, api_key: Optional[str]) -> dict:
        if not api_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")
        if api_key not in self.valid_keys:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
        return self.valid_keys[api_key]


api_key_auth = ApiKeyAuth()


def require_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
) -> dict:
    """Verify an API key and attach org/user metadata to the request."""
    context = api_key_auth.authenticate(x_api_key)
    request.state.org_id = context["org_id"]
    request.state.user_id = context["user_id"]
    return context


__all__ = ["ApiKeyAuth", "require_api_key"]
