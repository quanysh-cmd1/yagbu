from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/v1/chat", tags=["inference"])


@router.post("/completions")
def chat_completions(payload: dict) -> dict:
    """
    OpenAI-compatible chat completion endpoint.
    Returns streaming or non-streaming response.
    """
    model = payload.get("model")
    messages = payload.get("messages", [])
    max_tokens = payload.get("max_tokens", 128)
    stream = payload.get("stream", False)

    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="model is required",
        )

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="messages is required",
        )

    # Stub response
    return {
        "id": "chatcmpl-yagbu",
        "object": "chat.completion",
        "created": 1234567890,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"YAGBU response for model={model} with max_tokens={max_tokens}",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": len(str(messages)),
            "completion_tokens": max_tokens,
            "total_tokens": len(str(messages)) + max_tokens,
        },
    }


@router.post("/completions/async")
def async_completion(payload: dict) -> dict:
    """
    Asynchronous inference job.
    Returns job_id for polling.
    """
    return {
        "job_id": "job-async-123",
        "status": "queued",
        "model": payload.get("model"),
        "created_at": "2026-10-02T06:30:00Z",
    }


__all__ = ["router"]
