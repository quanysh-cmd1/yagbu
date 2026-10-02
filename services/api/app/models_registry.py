from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Adapter(Base):
    __tablename__ = "adapters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    org_id: Mapped[Optional[str]] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    model_id: Mapped[Optional[str]] = mapped_column(ForeignKey("models.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    adapter_type: Mapped[str] = mapped_column(String(64), nullable=False)  # lora, prerouter, recover
    path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    version: Mapped[str] = mapped_column(String(64), default="1.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    org_id: Mapped[Optional[str]] = mapped_column(ForeignKey("organizations.id"), nullable=True)
    model_id: Mapped[Optional[str]] = mapped_column(ForeignKey("models.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(64), default="stopped")  # stopped, starting, running, stopping, failed
    region: Mapped[str] = mapped_column(String(128), default="us-east-1")
    replica_count: Mapped[int] = mapped_column(Integer, default=1)
    memory_mb: Mapped[int] = mapped_column(Integer, default=2048)
    max_batch_size: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class DeploymentMetrics(Base):
    __tablename__ = "deployment_metrics"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    deployment_id: Mapped[Optional[str]] = mapped_column(ForeignKey("deployments.id"), nullable=True)
    requests_total: Mapped[int] = mapped_column(Integer, default=0)
    requests_success: Mapped[int] = mapped_column(Integer, default=0)
    requests_failed: Mapped[int] = mapped_column(Integer, default=0)
    avg_latency_ms: Mapped[float] = mapped_column(default=0.0)
    tokens_generated: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


__all__ = ["Adapter", "Deployment", "DeploymentMetrics"]
