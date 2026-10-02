from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class InferenceRequestMessage(BaseModel):
    role: str  # user, assistant, system
    content: str


class InferenceRequest(BaseModel):
    model: str  # model_id or deployment_id
    messages: list[InferenceRequestMessage]
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False


class InferenceResponseChoice(BaseModel):
    index: int
    message: InferenceRequestMessage
    finish_reason: str  # stop, length, error


class InferenceResponse(BaseModel):
    id: str
    model: str
    choices: list[InferenceResponseChoice]
    usage: dict  # {prompt_tokens, completion_tokens, total_tokens}
    created_at: str


class JobCreate(BaseModel):
    deployment_id: str
    job_type: str = "chat"  # chat, completion, batch
    payload: dict


class JobRead(BaseModel):
    id: str
    deployment_id: str
    job_type: str
    status: str  # queued, running, completed, failed
    created_at: str


__all__ = [
    "InferenceRequestMessage",
    "InferenceRequest",
    "InferenceResponseChoice",
    "InferenceResponse",
    "JobCreate",
    "JobRead",
]
