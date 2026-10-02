from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except Exception:  # pragma: no cover - optional dependency path
    FastAPI = None
    BaseModel = object

from .runtime import ChatMessage, StreamingRuntime


if FastAPI is not None:
    class ChatRequestModel(BaseModel):
        model: Optional[str] = None
        messages: List[Dict[str, str]] = Field(...)
        max_tokens: int = 128
        temperature: float = 0.7
        stream: bool = False


    def create_app(runtime_factory: Optional[Callable[[], StreamingRuntime]] = None) -> FastAPI:
        app = FastAPI(title="YAGBU", version="0.1.0")

        @app.get("/health")
        def health() -> Dict[str, str]:
            return {"status": "ok", "service": "yagbu"}

        @app.post("/v1/chat/completions")
        def chat_completions(payload: ChatRequestModel):
            runtime = runtime_factory() if runtime_factory is not None else StreamingRuntime(model_dir="./models")
            text = runtime.chat(payload.messages, max_tokens=payload.max_tokens)
            return {
                "id": "chatcmpl-yagbu",
                "object": "chat.completion",
                "model": payload.model or runtime.model_spec.name,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": text},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            }

        return app
else:
    def create_app(runtime_factory: Optional[Callable[[], StreamingRuntime]] = None) -> Any:
        raise RuntimeError("FastAPI is required for the YAGBU server. Install yagbu[serve].")


__all__ = ["create_app", "ChatRequestModel"]
