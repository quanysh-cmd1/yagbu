from __future__ import annotations

from pydantic import BaseModel, Field


class BillingPlanCreate(BaseModel):
    name: str
    slug: str
    price_monthly: float = 0.0
    token_price: float = 0.0
    request_limit: int = 0
    is_default: bool = False


class BillingPlanRead(BaseModel):
    id: str
    name: str
    slug: str
    price_monthly: float
    token_price: float
    request_limit: int
    is_default: bool


class SubscriptionRead(BaseModel):
    id: str
    org_id: str | None
    plan_id: str | None
    status: str
    started_at: str | None = None
    ends_at: str | None = None


class InvoiceRead(BaseModel):
    id: str
    org_id: str | None
    invoice_number: str
    amount: float
    currency: str
    status: str


__all__ = ["BillingPlanCreate", "BillingPlanRead", "SubscriptionRead", "InvoiceRead"]
