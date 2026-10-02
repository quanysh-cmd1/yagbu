from __future__ import annotations

import asyncio
import random
from typing import Any, Callable


class RetryPolicy:
    """A tiny retry helper with exponential backoff."""

    def __init__(self, max_retries: int = 3, base_delay: float = 0.25, max_delay: float = 5.0) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def run(self, fn: Callable[[], Any], *, jitter: float = 0.1) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                return await fn() if asyncio.iscoroutinefunction(fn) else fn()
            except Exception as exc:  # pragma: no cover - basic retry shim
                last_error = exc
                if attempt >= self.max_retries:
                    raise
                delay = min(self.base_delay * (2**attempt), self.max_delay)
                delay += random.uniform(0, jitter)
                await asyncio.sleep(delay)
        if last_error is not None:
            raise last_error
        raise RuntimeError("Retry policy exhausted without error")


retry_policy = RetryPolicy()


__all__ = ["RetryPolicy", "retry_policy"]
