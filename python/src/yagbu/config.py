from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ModelConfig:
    model_dir: str
    family: str = "llama"
    quantization: str = "int4"
    max_context: int = 4096
    adapter_dir: Optional[str] = None


def resolve_model_dir(model_dir: str) -> Path:
    path = Path(model_dir).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Model directory does not exist: {path}")
    return path
