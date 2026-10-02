from __future__ import annotations

from fastapi import FastAPI

from .routers.admin import router as admin_router
from .routers.admin_ui import router as admin_ui_router
from .routers.auth import router as auth_router
from .routers.billing import router as billing_router
from .routers.deployments import router as deployments_router
from .routers.health import router as health_router
from .routers.inference import router as inference_router
from .routers.jobs import router as jobs_router
from .routers.model_registry import router as model_registry_router
from .routers.models import router as models_router
from .routers.monitoring import router as monitoring_router
from .routers.usage import router as usage_router

app = FastAPI(
    title="YAGBU API",
    version="0.5.0",
    description="Production-oriented SaaS API for YAGBU",
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(model_registry_router)
app.include_router(deployments_router)
app.include_router(inference_router)
app.include_router(jobs_router)
app.include_router(models_router)
app.include_router(usage_router)
app.include_router(billing_router)
app.include_router(admin_router)
app.include_router(admin_ui_router)
app.include_router(monitoring_router)


@app.get("/")
def root() -> dict:
    return {
        "service": "yagbu-api",
        "version": "0.5.0",
        "status": "ok",
        "dashboard": "/dashboard",
    }


__all__ = ["app"]
