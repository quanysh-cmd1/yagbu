from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any


@dataclass
class RateLimitPolicy:
    org_id: str
    per_minute: int = 60
    per_hour: int = 1200
    burst: int = 10


class SimpleRateLimiter:
    """A minimal in-memory rate limiter for per-org usage."""

    def __init__(self) -> None:
        self._history: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, org_id: str, policy: RateLimitPolicy) -> bool:
        now = time()
        window = 60.0
        with self._lock:
            bucket = self._history[org_id]
            while bucket and now - bucket[0] > window:
                bucket.popleft()

            if len(bucket) >= policy.per_minute:
                return False
            bucket.append(now)
            return True


rate_limiter = SimpleRateLimiter()


__all__ = ["RateLimitPolicy", "SimpleRateLimiter", "rate_limiter"]
