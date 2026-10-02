from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ModelSpec:
    name: str
    family: str
    path: Path
    quantization: str = "int4"
    supports_adapter: bool = True
    default_backend: str = "python"
    context_length: int = 4096
    adapter_dirs: List[str] = field(default_factory=list)


class ModelRegistry:
    """Simple registry that resolves local model directories to a model spec."""

    def __init__(self):
        self._models: Dict[str, ModelSpec] = {}

    def register(self, spec: ModelSpec) -> None:
        self._models[spec.name] = spec

    def resolve(self, model_dir: str | Path) -> ModelSpec:
        path = Path(model_dir).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Model directory does not exist: {path}")

        resolved_name = path.name
        if resolved_name in self._models:
            return self._models[resolved_name]

        family = "unknown"
        adapter_dirs: List[str] = []

        config_file = path / "config.json"
        if config_file.exists():
            try:
                with config_file.open("r", encoding="utf-8") as fh:
                    payload = json.load(fh)
                family = str(payload.get("model_type") or payload.get("family") or payload.get("architecture") or family).lower()
            except Exception:
                pass

        for candidate in ["lora", "adapters", "adapter", "artifacts"]:
            candidate_dir = path / candidate
            if candidate_dir.exists():
                adapter_dirs.append(str(candidate_dir))

        spec = ModelSpec(
            name=resolved_name,
            family=family,
            path=path,
            quantization="int4",
            supports_adapter=bool(adapter_dirs) or True,
            default_backend="python",
            context_length=4096,
            adapter_dirs=adapter_dirs,
        )
        self.register(spec)
        return spec

    def available(self) -> List[str]:
        return sorted(self._models.keys())


DEFAULT_REGISTRY = ModelRegistry()
