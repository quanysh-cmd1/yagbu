from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class AdapterSpec:
    """Adapter specification: metadata for a single adapter unit."""

    name: str
    adapter_type: str = "lora"  # lora, recover, prerouter
    path: Optional[Path] = None
    dtype: str = "int4"
    trainable: bool = False
    source: str = "unknown"  # training source or model checkpoint
    version: str = "1.0"
    owner_layers: Optional[List[int]] = None  # which layers this adapter serves


class AdapterManager:
    """Manages adapter discovery, loading, and lifecycle for a model runtime."""

    def __init__(self, model_dir: str | Path):
        self.model_dir = Path(model_dir).expanduser().resolve()
        self._adapters: Dict[str, AdapterSpec] = {}
        self._discover_adapters()

    def _discover_adapters(self) -> None:
        """Scan model directory for standard adapter files."""
        if not self.model_dir.exists():
            return

        # Standard LoRA adapter patterns
        lora_patterns = ["lora_*.safetensors", "*_lora.safetensors"]
        for pattern in lora_patterns:
            for path in self.model_dir.glob(pattern):
                spec = AdapterSpec(
                    name=path.stem,
                    adapter_type="lora",
                    path=path,
                    dtype="int4",
                )
                self._adapters[path.stem] = spec

        # Prerouter adapter patterns
        prerouter_patterns = ["prerouter_*.safetensors", "*_prerouter.safetensors"]
        for pattern in prerouter_patterns:
            for path in self.model_dir.glob(pattern):
                spec = AdapterSpec(
                    name=path.stem,
                    adapter_type="prerouter",
                    path=path,
                    dtype="int4",
                )
                self._adapters[path.stem] = spec

        # Recover-style adapters (alternative naming)
        recover_patterns = ["recover_*.safetensors", "*_recover.safetensors"]
        for pattern in recover_patterns:
            for path in self.model_dir.glob(pattern):
                spec = AdapterSpec(
                    name=path.stem,
                    adapter_type="recover",
                    path=path,
                    dtype="int4",
                )
                self._adapters[path.stem] = spec

    def list_adapters(self) -> List[str]:
        """Return list of available adapter names."""
        return sorted(self._adapters.keys())

    def get_adapter(self, name: str) -> Optional[AdapterSpec]:
        """Retrieve an adapter by name."""
        return self._adapters.get(name)

    def get_by_type(self, adapter_type: str) -> List[AdapterSpec]:
        """Get all adapters of a specific type."""
        return [spec for spec in self._adapters.values() if spec.adapter_type == adapter_type]

    def load_adapter_config(self, name: str) -> Optional[Dict]:
        """Load adapter metadata from filesystem if available."""
        spec = self.get_adapter(name)
        if not spec or not spec.path or not spec.path.exists():
            return None

        # Stub: in a real implementation, parse safetensors header for metadata
        return {
            "name": spec.name,
            "type": spec.adapter_type,
            "dtype": spec.dtype,
            "source": spec.source,
            "version": spec.version,
        }

    def activate_adapters(self, names: List[str]) -> List[AdapterSpec]:
        """Mark a list of adapters as active for the current session."""
        active = []
        for name in names:
            spec = self.get_adapter(name)
            if spec:
                active.append(spec)
        return active

    def has_adapters(self) -> bool:
        """Check if any adapters are available."""
        return bool(self._adapters)


__all__ = ["AdapterSpec", "AdapterManager"]
