from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Any


@dataclass
class DLQMessage:
    key: str
    payload: Any
    error: str
    created_at: float


class DeadLetterQueue:
    """Simple in-memory dead-letter queue for failed workload retries."""

    def __init__(self, max_items: int = 1000) -> None:
        self.max_items = max_items
        self._messages: deque[DLQMessage] = deque(maxlen=max_items)
        self._lock = Lock()

    def push(self, *, key: str, payload: Any, error: str) -> DLQMessage:
        item = DLQMessage(key=key, payload=payload, error=error, created_at=time())
        with self._lock:
            self._messages.append(item)
        return item

    def list(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                {"key": item.key, "payload": item.payload, "error": item.error, "created_at": item.created_at}
                for item in self._messages
            ]


dead_letter_queue = DeadLetterQueue()


__all__ = ["DLQMessage", "DeadLetterQueue", "dead_letter_queue"]
