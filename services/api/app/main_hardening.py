from __future__ import annotations

from fastapi import FastAPI

from .routers.reliability import router as reliability_router

app = FastAPI(
    title="YAGBU API",
    version="0.8.0",
    description="Production-hardening layer for reliability, rate-limits, DLQ, and SLO monitoring",
)

app.include_router(reliability_router)


@app.get("/")
def root() -> dict:
    return {
        "service": "yagbu-api",
        "version": "0.8.0",
        "status": "ok",
        "reliability": "/v1/reliability/health",
    }


__all__ = ["app"]
