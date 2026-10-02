from __future__ import annotations

from fastapi import FastAPI

from .routers.auth import router as auth_router
from .routers.health import router as health_router
from .routers.models import router as models_router

app = FastAPI(title="YAGBU API", version="0.1.0")
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(models_router)


@app.get("/")
def root() -> dict:
    return {"service": "yagbu-api", "status": "ok"}


__all__ = ["app"]
