from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from .dead_letter import dead_letter_queue
from .monitoring_alerts import monitoring_snapshot
from .rate_limit import RateLimitPolicy, rate_limiter

router = APIRouter(prefix="/v1/reliability", tags=["reliability"])


@router.get("/rate-limit")
def rate_limit_check(
    org_id: str = Query(..., description="Organization ID"),
    policy_per_minute: int = Query(60, description="Requests per minute"),
) -> dict:
    policy = RateLimitPolicy(org_id=org_id, per_minute=policy_per_minute)
    allowed = rate_limiter.allow(org_id=org_id, policy=policy)
    return {"org_id": org_id, "allowed": allowed, "policy": {"per_minute": policy.per_minute}}


@router.get("/dlq")
def dead_letter_items() -> dict:
    return {"items": dead_letter_queue.list()}


@router.get("/slo")
def slo_summary() -> dict:
    return monitoring_snapshot.snapshot()


@router.post("/dlq/push")
def push_dlq(key: str, payload: dict, error: str) -> dict:
    item = dead_letter_queue.push(key=key, payload=payload, error=error)
    return {"accepted": True, "item": {"key": item.key, "error": item.error}}


@router.get("/health")
def reliability_health() -> dict:
    return {"status": "ok", "checks": ["rate_limit", "dlq", "slo", "retries"]}


__all__ = ["router"]
