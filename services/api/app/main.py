from __future__ import annotations

from fastapi import FastAPI

from .routers.auth import router as auth_router
from .routers.deployments import router as deployments_router
from .routers.health import router as health_router
from .routers.inference import router as inference_router
from .routers.jobs import router as jobs_router
from .routers.model_registry import router as model_registry_router
from .routers.models import router as models_router

app = FastAPI(
    title="YAGBU API",
    version="0.4.2",
    description="Open-source SaaS inference platform for Llama and OSS models",
)

# Health and basic routes
app.include_router(health_router)
app.include_router(auth_router)

# Model registry and deployment routes
app.include_router(model_registry_router)
app.include_router(deployments_router)

# Inference and job routes
app.include_router(inference_router)
app.include_router(jobs_router)

# Legacy models endpoint
app.include_router(models_router)


@app.get("/")
def root() -> dict:
    return {
        "service": "yagbu-api",
        "version": "0.4.2",
        "status": "ok",
        "docs": "/docs",
    }


__all__ = ["app"]
