from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from .api_auth import require_api_key
from .commercial import (
    PLAN_CATALOG,
    create_invoice,
    create_support_ticket,
    ensure_subscription,
    get_entitlements,
    get_plan,
    get_subscription,
    list_invoices,
    preview_invoice,
)

router = APIRouter(prefix="/v1/billing", tags=["billing"])


@router.get("/plans")
def billing_plans(context: dict = Depends(require_api_key)) -> dict:
    return {
        "plans": [
            {
                "id": plan.id,
                "name": plan.name,
                "price_monthly": plan.monthly_price,
                "token_price": plan.token_price,
                "included_tokens": plan.included_tokens,
                "api_limit_per_minute": plan.api_limit_per_minute,
                "features": plan.features,
            }
            for plan in PLAN_CATALOG.values()
        ],
        "org_id": context["org_id"],
    }


@router.get("/subscriptions")
def billing_subscription(context: dict = Depends(require_api_key)) -> dict:
    subscription = get_subscription(context["org_id"])
    return {
        "org_id": context["org_id"],
        "subscription": {
            "plan_id": subscription.plan_id,
            "status": subscription.status,
            "created_at": subscription.created_at.isoformat(),
            "current_period_end": subscription.current_period_end.isoformat(),
        },
    }


@router.post("/subscriptions/assign")
def assign_subscription(
    plan_id: str,
    context: dict = Depends(require_api_key),
) -> dict:
    try:
        get_plan(plan_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    subscription = ensure_subscription(context["org_id"], plan_id)
    subscription.plan_id = plan_id
    subscription.status = "active"
    return {
        "org_id": context["org_id"],
        "subscription": {
            "plan_id": subscription.plan_id,
            "status": subscription.status,
            "current_period_end": subscription.current_period_end.isoformat(),
        },
    }


@router.get("/entitlements")
def billing_entitlements(context: dict = Depends(require_api_key)) -> dict:
    return get_entitlements(context["org_id"])


@router.get("/invoices")
def billing_invoices(
    context: dict = Depends(require_api_key),
    status_filter: str | None = Query(default=None, alias="status"),
) -> dict:
    invoices = list_invoices(context["org_id"])
    if status_filter:
        invoices = [invoice for invoice in invoices if invoice["status"] == status_filter]
    return {"invoices": invoices, "org_id": context["org_id"]}


@router.post("/invoices/preview")
def preview_billing_invoice(
    usage_tokens: int = 0,
    usage_requests: int = 0,
    context: dict = Depends(require_api_key),
) -> dict:
    preview = preview_invoice(context["org_id"], usage_tokens=usage_tokens, usage_requests=usage_requests)
    return preview


@router.post("/invoices/create")
def create_billing_invoice(
    usage_tokens: int = 0,
    usage_requests: int = 0,
    context: dict = Depends(require_api_key),
) -> dict:
    invoice = create_invoice(context["org_id"], usage_tokens=usage_tokens, usage_requests=usage_requests)
    return {
        "invoice_id": invoice.invoice_id,
        "org_id": context["org_id"],
        "amount": invoice.amount,
        "currency": invoice.currency,
        "status": invoice.status,
    }


@router.get("/support")
def support_tickets(context: dict = Depends(require_api_key)) -> dict:
    return {"org_id": context["org_id"], "tickets": []}


@router.post("/support")
def create_support_ticket_route(
    title: str,
    description: str,
    priority: str = "normal",
    context: dict = Depends(require_api_key),
) -> dict:
    ticket = create_support_ticket(context["org_id"], title=title, description=description, priority=priority)
    return {"ticket": ticket}


__all__ = ["router"]
