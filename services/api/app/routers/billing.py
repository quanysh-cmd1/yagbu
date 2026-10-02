from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass(frozen=True)
class Plan:
    id: str
    name: str
    monthly_price: float
    token_price: float
    included_tokens: int
    api_limit_per_minute: int
    features: list[str]


@dataclass
class Subscription:
    org_id: str
    plan_id: str
    status: str
    created_at: datetime
    current_period_end: datetime
    usage_tokens: int = 0
    usage_requests: int = 0


@dataclass
class Invoice:
    invoice_id: str
    org_id: str
    plan_id: str
    status: str
    amount: float
    currency: str
    issue_date: datetime
    due_date: datetime
    usage_tokens: int = 0
    usage_requests: int = 0


PLAN_CATALOG: dict[str, Plan] = {
    "starter": Plan(
        id="starter",
        name="Starter",
        monthly_price=0.0,
        token_price=0.00005,
        included_tokens=100000,
        api_limit_per_minute=30,
        features=["Basic API access", "1 workspace", "Community support"],
    ),
    "pro": Plan(
        id="pro",
        name="Pro",
        monthly_price=29.0,
        token_price=0.00003,
        included_tokens=1000000,
        api_limit_per_minute=120,
        features=["Priority queue", "Unlimited prompts", "Email support"],
    ),
    "enterprise": Plan(
        id="enterprise",
        name="Enterprise",
        monthly_price=199.0,
        token_price=0.000015,
        included_tokens=10000000,
        api_limit_per_minute=500,
        features=["Dedicated SLA", "Custom onboarding", "Private support"],
    ),
}


SUBSCRIPTIONS: dict[str, Subscription] = {}
INVOICES: list[Invoice] = []
SUPPORT_TICKETS: list[dict[str, Any]] = []


def get_plan(plan_id: str) -> Plan:
    try:
        return PLAN_CATALOG[plan_id]
    except KeyError as exc:  # pragma: no cover - normal validation path
        raise ValueError(f"Unknown plan_id: {plan_id}") from exc


def ensure_subscription(org_id: str, plan_id: str = "starter") -> Subscription:
    existing = SUBSCRIPTIONS.get(org_id)
    if existing is not None:
        return existing

    plan = get_plan(plan_id)
    now = datetime.now(timezone.utc)
    sub = Subscription(
        org_id=org_id,
        plan_id=plan.id,
        status="active",
        created_at=now,
        current_period_end=now + timedelta(days=30),
    )
    SUBSCRIPTIONS[org_id] = sub
    return sub


def get_subscription(org_id: str) -> Subscription:
    return SUBSCRIPTIONS.get(org_id) or ensure_subscription(org_id)


def get_entitlements(org_id: str) -> dict[str, Any]:
    sub = get_subscription(org_id)
    plan = get_plan(sub.plan_id)
    return {
        "org_id": org_id,
        "plan_id": sub.plan_id,
        "status": sub.status,
        "included_tokens": plan.included_tokens,
        "token_price": plan.token_price,
        "api_limit_per_minute": plan.api_limit_per_minute,
        "features": plan.features,
    }


def preview_invoice(org_id: str, usage_tokens: int = 0, usage_requests: int = 0) -> dict[str, Any]:
    sub = get_subscription(org_id)
    plan = get_plan(sub.plan_id)
    base = plan.monthly_price
    extra_tokens = max(0, usage_tokens - plan.included_tokens)
    token_charge = extra_tokens * plan.token_price
    amount = round(base + token_charge, 2)
    return {
        "org_id": org_id,
        "plan_id": sub.plan_id,
        "amount": amount,
        "currency": "USD",
        "usage_tokens": usage_tokens,
        "usage_requests": usage_requests,
        "base_amount": base,
        "token_charge": round(token_charge, 2),
    }


def create_invoice(org_id: str, usage_tokens: int = 0, usage_requests: int = 0) -> Invoice:
    sub = get_subscription(org_id)
    plan = get_plan(sub.plan_id)
    preview = preview_invoice(org_id, usage_tokens=usage_tokens, usage_requests=usage_requests)
    now = datetime.now(timezone.utc)
    invoice = Invoice(
        invoice_id=f"inv-{len(INVOICES) + 1:04d}",
        org_id=org_id,
        plan_id=plan.id,
        status="issued",
        amount=preview["amount"],
        currency="USD",
        issue_date=now,
        due_date=now + timedelta(days=14),
        usage_tokens=usage_tokens,
        usage_requests=usage_requests,
    )
    INVOICES.append(invoice)
    return invoice


def list_invoices(org_id: str) -> list[dict[str, Any]]:
    return [
        {
            "invoice_id": inv.invoice_id,
            "org_id": inv.org_id,
            "plan_id": inv.plan_id,
            "status": inv.status,
            "amount": inv.amount,
            "currency": inv.currency,
            "issue_date": inv.issue_date.isoformat(),
            "due_date": inv.due_date.isoformat(),
            "usage_tokens": inv.usage_tokens,
            "usage_requests": inv.usage_requests,
        }
        for inv in INVOICES
        if inv.org_id == org_id
    ]


def create_support_ticket(org_id: str, title: str, description: str, priority: str = "normal") -> dict[str, Any]:
    ticket = {
        "ticket_id": f"ticket-{len(SUPPORT_TICKETS) + 1:04d}",
        "org_id": org_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    SUPPORT_TICKETS.append(ticket)
    return ticket


__all__ = [
    "PLAN_CATALOG",
    "Invoice",
    "Plan",
    "Subscription",
    "create_invoice",
    "create_support_ticket",
    "ensure_subscription",
    "get_entitlements",
    "get_plan",
    "get_subscription",
    "list_invoices",
    "preview_invoice",
]
