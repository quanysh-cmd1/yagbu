from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from .api_auth import require_api_key

router = APIRouter(prefix="/v1/usage", tags=["usage"])


@router.get("/summary")
def usage_summary(
    request: Request,
    context: dict = Depends(require_api_key),
) -> dict:
    return {
        "org_id": request.state.org_id,
        "user_id": request.state.user_id,
        "requests": 120,
        "tokens": 45678,
        "cost_usd": 12.34,
        "currency": "USD",
        "quota_remaining": 1000,
    }


@router.get("/events")
def usage_events(
    request: Request,
    context: dict = Depends(require_api_key),
) -> dict:
    return {
        "events": [
            {"type": "chat_completion", "tokens": 520, "cost_usd": 0.04, "created_at": "2026-10-02T06:00:00Z"},
            {"type": "chat_completion", "tokens": 1024, "cost_usd": 0.08, "created_at": "2026-10-02T06:05:00Z"},
        ],
        "org_id": request.state.org_id,
    }


__all__ = ["router"]
