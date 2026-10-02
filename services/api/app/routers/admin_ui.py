from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/admin", tags=["admin-ui"])


@router.get("/dashboard")
def admin_dashboard() -> dict:
    return {
        "org_name": "demo-org",
        "workspace": "default",
        "models": [
            {"name": "yagbu-8b", "status": "healthy", "deployments": 2},
            {"name": "yagbu-35b", "status": "healthy", "deployments": 1},
        ],
        "usage_this_month": {
            "requests": 12000,
            "tokens": 450000,
            "cost_usd": 78.4,
        },
    }


@router.get("/team")
def admin_team() -> dict:
    return {
        "members": [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob", "role": "developer"},
            {"name": "Charlie", "role": "analyst"},
        ]
    }


__all__ = ["router"]
