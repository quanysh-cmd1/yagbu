from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SLOMetric:
    name: str
    p95_ms: float
    p99_ms: float
    error_rate: float


class MonitoringSnapshot:
    def __init__(self) -> None:
        self.metrics: list[SLOMetric] = [
            SLOMetric(name="api_latency", p95_ms=240.0, p99_ms=450.0, error_rate=0.02),
            SLOMetric(name="job_queue", p95_ms=800.0, p99_ms=1500.0, error_rate=0.05),
            SLOMetric(name="inference", p95_ms=3000.0, p99_ms=5000.0, error_rate=0.03),
        ]

    def snapshot(self) -> dict[str, Any]:
        return {
            "metrics": [
                {"name": m.name, "p95_ms": m.p95_ms, "p99_ms": m.p99_ms, "error_rate": m.error_rate}
                for m in self.metrics
            ]
        }


monitoring_snapshot = MonitoringSnapshot()


__all__ = ["SLOMetric", "MonitoringSnapshot", "monitoring_snapshot"]
