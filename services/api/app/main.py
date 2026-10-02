from __future__ import annotations

from fastapi import FastAPI

from .routers.admin import router as admin_router
from .routers.auth import router as auth_router
from .routers.billing import router as billing_router
from .routers.deployments import router as deployments_router
from .routers.health import router as health_router
from .routers.inference import router as inference_router
from .routers.jobs import router as jobs_router
from .routers.model_registry import router as model_registry_router
from .routers.models import router as models_router
from .routers.usage import router as usage_router

app = FastAPI(
    title="YAGBU API",
    version="0.4.3",
    description="Open-source SaaS inference platform for Llama and OSS models",
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


@app.get("/")
def root() -> dict:
    return {
        "service": "yagbu-api",
        "version": "0.4.3",
        "status": "ok",
        "docs": "/docs",
    }


__all__ = ["app"]
