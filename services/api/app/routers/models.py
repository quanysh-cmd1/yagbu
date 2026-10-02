from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def list_models() -> dict:
    return {
        "models": [
            {"name": "yagbu-8b", "family": "llama", "status": "available"},
            {"name": "yagbu-35b", "family": "llama", "status": "available"},
        ]
    }


__all__ = ["router"]
