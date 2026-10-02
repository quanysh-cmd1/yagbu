from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class AdapterConfig:
    name: str = "lora"
    enabled: bool = True
    path: Optional[str] = None
    dtype: str = "int4"


@dataclass
class GenerationConfig:
    max_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = True
    stop: Optional[List[str]] = None


@dataclass
class ModelConfig:
    model_dir: str
    family: str = "llama"
    quantization: str = "int4"
    max_context: int = 4096
    adapter_dir: Optional[str] = None
    backend: str = "python"
    adapter: AdapterConfig = field(default_factory=AdapterConfig)


def resolve_model_dir(model_dir: str) -> Path:
    path = Path(model_dir).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Model directory does not exist: {path}")
    return path


def detect_model_family(model_dir: str | Path) -> str:
    path = Path(model_dir)
    if not path.exists():
        return "unknown"

    config_file = path / "config.json"
    if config_file.exists():
        try:
            import json

            with config_file.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            family = str(payload.get("model_type") or payload.get("family") or payload.get("architecture") or "").lower()
            if family:
                return family
        except Exception:
            pass

    names = [p.name.lower() for p in path.iterdir() if p.is_dir() or p.is_file()]
    for token in ("qwen", "llama", "mistral", "deepseek", "phi"):
        if any(token in name for name in names):
            return token

    return "llama"


def load_model_config(model_dir: str) -> ModelConfig:
    resolved = resolve_model_dir(model_dir)
    family = detect_model_family(resolved)
    return ModelConfig(
        model_dir=str(resolved),
        family=family,
        quantization="int4",
        max_context=4096,
        backend="python",
    )
