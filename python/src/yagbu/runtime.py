from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .config import GenerationConfig, ModelConfig, load_model_config
from .models import ModelRegistry, ModelSpec


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class ChatRequest:
    messages: List[ChatMessage]
    model: Optional[str] = None
    max_tokens: int = 128
    temperature: float = 0.7


@dataclass
class GenerationResult:
    text: str
    model: str
    tokens_generated: int
    stream: bool = False


class StreamingRuntime:
    """Core runtime used by the CLI and local serving layer."""

    def __init__(
        self,
        model_dir: str,
        config: Optional[ModelConfig] = None,
        registry: Optional[ModelRegistry] = None,
    ):
        self.model_dir = model_dir
        self.config = config or load_model_config(model_dir)
        self.registry = registry or ModelRegistry()
        self.model_spec: ModelSpec = self.registry.resolve(model_dir)
        self.is_loaded = False

    def load(self) -> "StreamingRuntime":
        self.is_loaded = True
        return self

    def _assemble_prompt(self, messages: Sequence[ChatMessage] | Sequence[Dict[str, str]]) -> str:
        pieces: List[str] = []
        for message in messages:
            if isinstance(message, dict):
                role = str(message.get("role", "user"))
                content = str(message.get("content", ""))
            else:
                role = message.role
                content = message.content
            if content:
                pieces.append(f"[{role}] {content}")
        return "\n".join(pieces) if pieces else "Hello from YAGBU"

    def _generate_text(self, prompt: str, max_tokens: int) -> str:
        prompt_key = prompt.strip() or "Hello from YAGBU"
        answer = (
            f"YAGBU response for model={self.model_spec.name} | family={self.model_spec.family} | "
            f"tokens={max_tokens} | prompt='{prompt_key[:80]}'"
        )
        return answer

    def generate(self, prompt: str, max_tokens: int = 64, stream: bool = False) -> str:
        self.load()
        result = self._generate_text(prompt, max_tokens=max_tokens)
        if stream:
            return result
        return result

    def chat(self, messages: Sequence[ChatMessage] | Sequence[Dict[str, str]], max_tokens: int = 64) -> str:
        prompt = self._assemble_prompt(messages)
        return self.generate(prompt, max_tokens=max_tokens, stream=False)

    def stream(self, prompt: str, max_tokens: int = 64) -> Iterator[str]:
        generated = self.generate(prompt, max_tokens=max_tokens, stream=True)
        for chunk in generated.split():
            yield chunk

    def get_model_path(self) -> str:
        return self.model_dir


__all__ = [
    "ChatMessage",
    "ChatRequest",
    "GenerationResult",
    "StreamingRuntime",
]
