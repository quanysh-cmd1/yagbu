from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status

from .api_auth import require_api_key

router = APIRouter(prefix="/v1/billing", tags=["billing"])


@router.get("/plans")
def billing_plans(
    context: dict = Depends(require_api_key),
) -> dict:
    return {
        "plans": [
            {"id": "starter", "name": "Starter", "price_monthly": 0.0, "token_price": 0.0},
            {"id": "pro", "name": "Pro", "price_monthly": 29.0, "token_price": 0.0001},
        ],
        "org_id": context["org_id"],
    }


@router.get("/invoices")
def billing_invoices(
    context: dict = Depends(require_api_key),
) -> dict:
    return {
        "invoices": [
            {"id": "inv-001", "amount": 12.34, "currency": "USD", "status": "paid"},
        ],
        "org_id": context["org_id"],
    }


__all__ = ["router"]
