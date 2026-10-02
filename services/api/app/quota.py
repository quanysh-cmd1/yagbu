from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuotaPolicy:
    org_id: str
    requests_per_minute: int = 60
    requests_per_day: int = 10000
    tokens_per_day: int = 200000


def quota_check(policy: QuotaPolicy, requests_used: int, tokens_used: int) -> dict:
    status = "ok"
    if requests_used > policy.requests_per_day:
        status = "requests_exceeded"
    if tokens_used > policy.tokens_per_day:
        status = "tokens_exceeded"
    return {
        "org_id": policy.org_id,
        "status": status,
        "requests_used": requests_used,
        "requests_limit": policy.requests_per_day,
        "tokens_used": tokens_used,
        "tokens_limit": policy.tokens_per_day,
    }


__all__ = ["QuotaPolicy", "quota_check"]
