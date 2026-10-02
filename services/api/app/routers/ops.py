from __future__ import annotations

from fastapi import APIRouter, Depends

from .admin_auth import require_admin

router = APIRouter(prefix="/ops", tags=["ops"])


@router.get("/readiness")
def readiness() -> dict:
    return {"status": "ready"}


@router.get("/liveness")
def liveness() -> dict:
    return {"status": "alive"}


@router.get("/admin")
def admin_ops(admin=Depends(require_admin)) -> dict:
    return {
        "status": "ok",
        "admin": admin,
        "services": ["api", "worker", "db", "redis"],
    }


__all__ = ["router"]
