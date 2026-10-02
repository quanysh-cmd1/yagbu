from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/monitor", tags=["monitoring"])


@router.get("/overview")
def monitor_overview() -> dict:
    return {
        "status": "healthy",
        "uptime_hours": 24,
        "active_deployments": 3,
        "jobs_queued": 5,
        "jobs_failed_last_24h": 2,
    }


@router.get("/traces")
def traces() -> dict:
    return {
        "trace_count": 124,
        "latency_ms": {"p50": 500, "p95": 1800, "p99": 3500},
        "errors": 2,
    }


@router.get("/alerts")
def alerts() -> dict:
    return {
        "alerts": [
            {"level": "warning", "message": "Queue backlog increased 15% in the last hour"},
            {"level": "info", "message": "Model health check passing for yagbu-8b"},
        ]
    }


__all__ = ["router"]
