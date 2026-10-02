from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class AuditLogStore:
    """Very small in-memory audit log for multitenant visibility."""

    _events: list[dict[str, Any]] = []

    @classmethod
    def log_event(cls, *, org_id: str, user_id: str, action: str, resource: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "org_id": org_id,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
        }
        cls._events.append(event)
        return event

    @classmethod
    def list_events(cls, org_id: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        events = cls._events
        if org_id:
            events = [e for e in events if e["org_id"] == org_id]
        return events[-limit:]


__all__ = ["AuditLogStore"]
