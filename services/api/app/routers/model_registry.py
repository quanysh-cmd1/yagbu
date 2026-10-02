from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/v1/models", tags=["model-registry"])


@router.get("")
def list_models(org_id: str | None = None) -> dict:
    """
    List all available models for an organization.
    """
    return {
        "models": [
            {
                "id": "model-8b",
                "name": "yagbu-8b-preview",
                "family": "llama",
                "version": "1.0",
                "status": "available",
            },
            {
                "id": "model-35b",
                "name": "yagbu-35b-preview",
                "family": "llama",
                "version": "1.0",
                "status": "available",
            },
        ]
    }


@router.get("/{model_id}")
def get_model(model_id: str) -> dict:
    """
    Get details of a specific model.
    """
    return {
        "id": model_id,
        "name": "yagbu-8b-preview",
        "family": "llama",
        "version": "1.0",
        "status": "available",
        "max_context_length": 4096,
        "quantization": "int4",
    }


@router.post("/{model_id}/register-adapter")
def register_adapter(model_id: str, payload: dict) -> dict:
    """
    Register a new adapter (LoRA, prerouter, recover) for a model.
    """
    return {
        "adapter_id": f"adapter-{payload.get('name', 'unknown')}",
        "model_id": model_id,
        "type": payload.get("type", "unknown"),
        "status": "registered",
    }


__all__ = ["router"]
