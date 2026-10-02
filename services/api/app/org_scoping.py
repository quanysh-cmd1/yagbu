from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrgScope:
    org_id: str
    role: str = "viewer"
    user_id: str = "system"


def resolve_org_scope(x_org_id: str | None, x_user_id: str | None, x_role: str | None) -> OrgScope:
    org_id = x_org_id or "default-org"
    user_id = x_user_id or "system-user"
    role = x_role or "viewer"
    return OrgScope(org_id=org_id, role=role, user_id=user_id)


__all__ = ["OrgScope", "resolve_org_scope"]
