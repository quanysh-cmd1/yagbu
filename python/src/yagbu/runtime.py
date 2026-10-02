from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import ModelConfig, resolve_model_dir


class StreamingRuntime:
    """Core runtime stub for YAGBU. This is the foundational inference loop abstraction."""

    def __init__(self, model_dir: str, config: Optional[ModelConfig] = None):
        self.model_dir = resolve_model_dir(model_dir)
        self.config = config or ModelConfig(model_dir=str(self.model_dir))
        self._state: Dict[str, Any] = {}

    def load(self) -> "StreamingRuntime":
        self._state["loaded"] = True
        return self

    def generate(self, prompt: str, max_tokens: int = 64) -> str:
        if not self._state.get("loaded"):
            self.load()

        tokens = self._tokenize(prompt)
        generated = " ".join(["generated", "for", str(len(tokens)), "input", "tokens"])
        return f"{prompt} -> {generated} [max_tokens={max_tokens}]"

    def _tokenize(self, text: str) -> List[str]:
        return text.strip().split()

    def get_model_path(self) -> Path:
        return self.model_dir
