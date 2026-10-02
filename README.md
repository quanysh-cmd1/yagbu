# YAGBU

YAGBU is an open-source streaming inference framework for Llama and ChatGPT OSS models with SSD expert offload, Recover-LoRA style adapters, and routing prediction. It is a lightweight alternative inspired by `edge0`, designed to run large sparse MoE and OSS decoder models efficiently on consumer hardware.

## Project vision

The goal of YAGBU is to provide one codebase and one recipe for running modern open models on desktop, mobile, and edge devices while keeping memory usage bounded by the active expert set instead of the full parameter footprint.

Core objectives:
- Open model portability: Llama 3.x, Qwen, Mistral, and ChatGPT OSS style checkpoints
- Efficient serve path: local inference, API layer, and batch generation
- Consumer hardware optimization: SSD-backed expert paging, quantized weights, adapter reuse
- Unified runtime: same model logic across Python, macOS, iOS, Android, and Windows

## Multi-stage implementation plan

### Stage 1 — Foundation and repository bootstrap
- Define repo structure, docs, architecture, and contributor workflow
- Set up Python package skeleton and local developer environment
- Add project metadata, CI, and code hygiene conventions
- Create initial reference model config and runtime stubs

### Stage 2 — Core model abstraction
- Build model registry and tier detection logic
- Add config parsing for model families and adapters
- Define interfaces for tokenizer, weights, routing, and generation
- Keep the system backend-agnostic to allow MLX/CUDA/Metal/C++ backends later

### Stage 3 — Streaming inference runtime
- Add generation loop, caching, and token streaming
- Implement expert scheduling abstraction for SSD or memory paging
- Introduce adapter loading (LoRA / Recover-LoRA style)
- Add benchmark and profiling hooks

### Stage 4 — Serving and API layer
- Create OpenAI-compatible chat completion API
- Add local server, prompt handling, and session state
- Support async generation and stream callbacks
- Provide CLI commands for demo, chat, and serve

### Stage 5 — Cross-platform portability
- Add platform-specific backend entries for macOS, iOS, Android, Windows
- Reuse shared model logic and unify memory and adapter handling
- Ensure app runtimes can run a pack model locally with minimal code duplication

### Stage 6 — Production readiness
- Add model validation, smoke tests, and integration checks
- Benchmark throughput and device limits
- Publish release notes and model compatibility matrix
- Prepare docs for contributors and maintainers

## Repository structure

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── ARCHITECTURE.md
│   └── ROADMAP.md
├── python/
│   ├── README.md
│   ├── pyproject.toml
│   ├── examples/
│   │   └── hello.py
│   └── src/
│       └── yagbu/
│           ├── __init__.py
│           ├── config.py
│           └── runtime.py
├── scripts/
│   └── bootstrap.sh
├── models/
├── android/
├── ios/
├── macos/
├── windows/
└── .github/
```

## Quick start

Python package is the primary development entry point.

```bash
cd python
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
python -m yagbu
```

Example:

```python
from yagbu.runtime import StreamingRuntime

runtime = StreamingRuntime(model_dir="/path/to/model")
print(runtime.generate("Hello from YAGBU"))
```

## Documentation

- `docs/ROADMAP.md` — full implementation roadmap
- `docs/ARCHITECTURE.md` — system design and runtime model
- `python/README.md` — Python package developer guide

## Status

The project is in initial bootstrap phase and is being structured as a multi-stage open-source inference framework with clear portability and production milestones.

## License

Apache License 2.0
