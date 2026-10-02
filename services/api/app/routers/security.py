from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request, status

from .audit_logs import AuditLogStore
from .auth_roles import UserRole, role_can_access
from .org_scoping import resolve_org_scope
from .quota import QuotaPolicy, quota_check

router = APIRouter(prefix="/v1/security", tags=["security"])


@router.get("/roles")
def list_roles() -> dict:
    return {
        "roles": [
            {"name": UserRole.ADMIN.value, "level": 5},
            {"name": UserRole.OWNER.value, "level": 4},
            {"name": UserRole.DEVELOPER.value, "level": 3},
            {"name": UserRole.ANALYST.value, "level": 2},
            {"name": UserRole.VIEWER.value, "level": 1},
        ]
    }


@router.post("/authorize")
def authorize_action(
    request: Request,
    payload: dict,
    x_org_id: str | None = Header(default=None, alias="x-org-id"),
    x_user_id: str | None = Header(default=None, alias="x-user-id"),
    x_role: str | None = Header(default=None, alias="x-role"),
) -> dict:
    scope = resolve_org_scope(x_org_id, x_user_id, x_role)
    required_role = payload.get("required_role", UserRole.VIEWER.value)
    user_role = payload.get("user_role", scope.role)

    allowed = role_can_access(required_role, user_role)
    if allowed:
        AuditLogStore.log_event(
            org_id=scope.org_id,
            user_id=scope.user_id,
            action="authorize",
            resource=payload.get("resource", "unknown"),
            details={"allowed": True, "required_role": required_role, "user_role": user_role},
        )
        return {"allowed": True, "org_id": scope.org_id, "role": user_role}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User role does not have access to this action",
    )


@router.get("/audit")
def audit_logs(request: Request, org_id: str | None = None) -> dict:
    org_filter = org_id or getattr(request.state, "org_id", None)
    return {"events": AuditLogStore.list_events(org_id=org_filter, limit=50)}


@router.get("/quota")
def quota_summary(
    org_id: str,
    requests_used: int = 0,
    tokens_used: int = 0,
) -> dict:
    policy = QuotaPolicy(org_id=org_id)
    return quota_check(policy, requests_used=requests_used, tokens_used=tokens_used)


__all__ = ["router"]
