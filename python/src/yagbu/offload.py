from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OffloadPolicy(Enum):
    """Expert offload scheduling strategy."""

    RESIDENT = "resident"  # All experts in RAM
    SSD_DEMAND = "ssd_demand"  # Load on demand from SSD
    HYBRID = "hybrid"  # Mix of resident and SSD
    STREAMING = "streaming"  # Progressive expert paging


@dataclass
class MemoryBudget:
    """Memory budget tracking for a session."""

    total_available_mb: int
    resident_experts_mb: int = 0
    kv_cache_mb: int = 0
    adapter_mb: int = 0
    buffer_mb: int = 0

    def used_mb(self) -> int:
        """Total memory used so far."""
        return (
            self.resident_experts_mb
            + self.kv_cache_mb
            + self.adapter_mb
            + self.buffer_mb
        )

    def available_mb(self) -> int:
        """Remaining available memory."""
        return max(0, self.total_available_mb - self.used_mb())

    def is_within_budget(self, needed_mb: int) -> bool:
        """Check if an allocation fits in the budget."""
        return needed_mb <= self.available_mb()


class SSDPageManager:
    """Manages expert paging from SSD and warmth scheduling."""

    def __init__(
        self,
        policy: OffloadPolicy = OffloadPolicy.SSD_DEMAND,
        ssd_path: Optional[str] = None,
        budget: Optional[MemoryBudget] = None,
    ):
        self.policy = policy
        self.ssd_path = ssd_path
        self.budget = budget or MemoryBudget(total_available_mb=2048)
        self._warm_cache: set = set()  # Expert indices currently warm
        self._page_requests: list = []  # Pending page I/O requests

    def schedule_expert_page_in(self, expert_idx: int, layer: int) -> None:
        """Request an expert to be paged into RAM."""
        key = (layer, expert_idx)
        if key not in self._warm_cache:
            self._page_requests.append(key)

    def mark_warm(self, expert_idx: int, layer: int) -> None:
        """Mark an expert as currently in RAM."""
        self._warm_cache.add((layer, expert_idx))

    def prefetch_experts(self, layer: int, expert_indices: list) -> None:
        """Prefetch a set of experts for upcoming computation."""
        for idx in expert_indices:
            self.schedule_expert_page_in(idx, layer)

    def is_warm(self, expert_idx: int, layer: int) -> bool:
        """Check if an expert is currently resident."""
        return (layer, expert_idx) in self._warm_cache

    def clear_cold_experts(self, keep_recent: int = 32) -> None:
        """Evict experts from RAM beyond the keep threshold."""
        if len(self._warm_cache) > keep_recent:
            self._warm_cache.clear()

    def get_page_requests(self) -> list:
        """Retrieve pending page I/O operations."""
        requests = self._page_requests[:]
        self._page_requests.clear()
        return requests

    def memory_usage_estimate(self, num_warm_experts: int, bytes_per_expert: int = 0) -> int:
        """Estimate memory consumed by warm experts."""
        return len(self._warm_cache) * (bytes_per_expert or 65536)  # Stub estimate


class ExpertOffloadStrategy:
    """High-level strategy for routing expert loads."""

    def __init__(
        self,
        num_experts_per_layer: int,
        num_active_experts: int,
        model_family: str = "llama",
    ):
        self.num_experts_per_layer = num_experts_per_layer
        self.num_active_experts = num_active_experts
        self.model_family = model_family
        self.page_manager = SSDPageManager()

    def predict_expert_selection(
        self, token_position: int, layer: int
    ) -> list:
        """Predict which experts will be routed to (for prefetch)."""
        # Stub: in a real implementation, use a learned prerouter head
        # For now, return a deterministic sample
        import hashlib

        seed = int(
            hashlib.md5(f"{token_position}_{layer}".encode()).hexdigest()[:8], 16
        )
        return list(
            range(
                seed % self.num_experts_per_layer,
                min(
                    seed % self.num_experts_per_layer + self.num_active_experts,
                    self.num_experts_per_layer,
                ),
            )
        )

    def schedule_prefetch(self, token_position: int, layer: int) -> None:
        """Schedule prefetch of upcoming expert loads."""
        predicted_experts = self.predict_expert_selection(token_position + 1, layer)
        self.page_manager.prefetch_experts(layer, predicted_experts)


__all__ = [
    "OffloadPolicy",
    "MemoryBudget",
    "SSDPageManager",
    "ExpertOffloadStrategy",
]
