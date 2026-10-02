from __future__ import annotations

import os
from typing import Any

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class SimpleQueue:
    """A lightweight queue abstraction for worker orchestration."""

    def __init__(self, redis_url: str = REDIS_URL):
        self.redis_url = redis_url
        self._items: list[dict[str, Any]] = []

    def enqueue(self, job_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        item = {"job_type": job_type, "payload": payload, "status": "queued"}
        self._items.append(item)
        return item

    def list_jobs(self) -> list[dict[str, Any]]:
        return self._items


queue = SimpleQueue()


__all__ = ["queue", "SimpleQueue"]
