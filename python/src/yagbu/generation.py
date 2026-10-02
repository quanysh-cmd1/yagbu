from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional

from .adapters import AdapterManager
from .offload import ExpertOffloadStrategy, MemoryBudget, OffloadPolicy


@dataclass
class TokenContext:
    """Context for a single token generation step."""

    token_id: int
    position: int
    logits: Optional[List[float]] = None
    sequence_length: int = 0


@dataclass
class GenerationConfig:
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    stream: bool = True
    stop_sequences: List[str] = field(default_factory=list)


class TokenStream:
    """Streaming token iterator with session metadata."""

    def __init__(self, tokens: List[str], metadata: Optional[Dict[str, Any]] = None):
        self.tokens = tokens
        self.metadata = metadata or {}
        self._index = 0

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self._index >= len(self.tokens):
            raise StopIteration
        token = self.tokens[self._index]
        self._index += 1
        return token

    def has_more(self) -> bool:
        return self._index < len(self.tokens)


class GenerationSession:
    """Manages a single generation session with state and adapters."""

    def __init__(
        self,
        model_dir: str,
        model_family: str = "llama",
        adapter_manager: Optional[AdapterManager] = None,
        offload_policy: OffloadPolicy = OffloadPolicy.SSD_DEMAND,
        memory_budget_mb: int = 2048,
    ):
        self.model_dir = model_dir
        self.model_family = model_family
        self.adapter_manager = adapter_manager or AdapterManager(model_dir)
        self.offload_policy = offload_policy
        self.memory_budget = MemoryBudget(total_available_mb=memory_budget_mb)
        self.expert_strategy = ExpertOffloadStrategy(
            num_experts_per_layer=256,  # Stub: detect from config
            num_active_experts=8,  # Stub: detect from config
            model_family=model_family,
        )
        self.session_state: Dict[str, Any] = {
            "token_count": 0,
            "prefill_done": False,
            "cache_active": False,
            "active_adapters": [],
        }

    def load_adapters(self, adapter_names: Optional[List[str]] = None) -> None:
        """Load and activate specified adapters."""
        if adapter_names is None:
            # Auto-detect all available adapters
            adapter_names = self.adapter_manager.list_adapters()

        active = self.adapter_manager.activate_adapters(adapter_names)
        self.session_state["active_adapters"] = [spec.name for spec in active]

    def prefill_prompt(self, prompt_tokens: List[int]) -> None:
        """Process the entire prompt at once (prefill phase)."""
        self.session_state["token_count"] = len(prompt_tokens)
        self.session_state["prefill_done"] = True

        # Schedule expert prefetch for decode phase
        for layer in range(32):  # Stub: detect layer count
            self.expert_strategy.schedule_prefetch(len(prompt_tokens), layer)

    def generate_tokens(
        self,
        num_tokens: int = 64,
        config: Optional[GenerationConfig] = None,
    ) -> TokenStream:
        """Generate tokens autoregressively with streaming."""
        config = config or GenerationConfig()
        generated = []

        for i in range(num_tokens):
            # Stub: in real impl, compute logits from model
            token_id = (i + 1) % 50000
            token_text = f"[token_{token_id}]"
            generated.append(token_text)

            # Update position-based prefetch
            if i % 4 == 0:  # Prefetch every 4 tokens
                for layer in range(32):
                    self.expert_strategy.schedule_prefetch(
                        self.session_state["token_count"] + i, layer
                    )

            self.session_state["token_count"] += 1

            if not config.stream:
                continue

        return TokenStream(generated, metadata={"model": self.model_family})

    def get_memory_status(self) -> Dict[str, int]:
        """Return current memory usage and budget."""
        return {
            "total_available_mb": self.memory_budget.total_available_mb,
            "used_mb": self.memory_budget.used_mb(),
            "available_mb": self.memory_budget.available_mb(),
            "resident_experts_mb": self.memory_budget.resident_experts_mb,
        }

    def close(self) -> None:
        """Finalize the session and release resources."""
        self.expert_strategy.page_manager.clear_cold_experts()
        self.session_state.clear()


__all__ = [
    "TokenContext",
    "GenerationConfig",
    "TokenStream",
    "GenerationSession",
]
