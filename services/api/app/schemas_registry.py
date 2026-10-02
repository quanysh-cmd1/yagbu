from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class AdapterCreate(BaseModel):
    name: str
    adapter_type: str  # lora, prerouter, recover
    path: Optional[str] = None
    version: str = "1.0"


class AdapterRead(BaseModel):
    id: str
    name: str
    adapter_type: str
    version: str


class DeploymentCreate(BaseModel):
    name: str
    model_id: str
    region: str = "us-east-1"
    replica_count: int = 1
    memory_mb: int = 2048
    max_batch_size: int = 1


class DeploymentRead(BaseModel):
    id: str
    name: str
    model_id: str
    status: str
    region: str
    replica_count: int
    memory_mb: int
    created_at: str


class DeploymentStatusUpdate(BaseModel):
    status: str  # stopped, starting, running, stopping


class DeploymentMetricsRead(BaseModel):
    deployment_id: str
    requests_total: int
    requests_success: int
    requests_failed: int
    avg_latency_ms: float
    tokens_generated: int


__all__ = [
    "AdapterCreate",
    "AdapterRead",
    "DeploymentCreate",
    "DeploymentRead",
    "DeploymentStatusUpdate",
    "DeploymentMetricsRead",
]
