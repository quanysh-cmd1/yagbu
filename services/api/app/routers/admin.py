from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request, status

router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.get("/usage")
def admin_usage(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="x-api-key"),
) -> dict:
    """
    Mock admin usage endpoint.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )
    return {
        "total_requests": 123,
        "total_tokens": 45678,
        "total_cost_usd": 12.34,
        "active_orgs": 5,
        "models": ["yagbu-8b", "yagbu-35b"],
    }


@router.get("/plans")
def admin_plans() -> dict:
    return {
        "plans": [
            {"name": "starter", "price_monthly": 0.0, "token_price": 0.0, "request_limit": 1000},
            {"name": "pro", "price_monthly": 29.0, "token_price": 0.0001, "request_limit": 100000},
        ]
    }


__all__ = ["router"]
