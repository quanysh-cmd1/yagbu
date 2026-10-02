# macOS YAGBU Runtime

## Overview

Desktop-grade inference runtime for macOS with Apple Silicon optimization. Runs 8B and 35B models locally with streaming generation and CLI tools.

## Platform specifics

- **Target**: macOS 12.1+
- **Processor**: Apple Silicon (M1/M2/M3/M4 recommended)
- **GPU**: Metal integration via MLX
- **Memory**: 8GB+ for 8B, 16GB+ for 35B
- **Storage**: Local SSD for expert paging

## Build and install

### From source (Rust)

```bash
cd macos
cargo build --release
```

Binary at `target/release/yagbu-macos`.

### Install to system

```bash
cargo install --path .
```

## Usage

### Chat

```bash
yagbu-macos chat --model-dir ./models/yagbu-8b
```

### Serve local API

```bash
yagbu-macos serve --model-dir ./models/yagbu-35b \
  --host 127.0.0.1 --port 8000

# Then:
curl http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Hello!"}],"max_tokens":32}'
```

### Benchmark

```bash
yagbu-macos bench --model-dir ./models/yagbu-8b
```

## Architecture

```
CLI / Daemon
   |
   v
Rust Runtime Wrapper
   |
   v
Python Backend (via FFI)
   |
   +-> MLX Inference
   +-> Expert Offload (NVMe)
   +-> Adapter Management
```

## Features

- Efficient Apple Silicon compute
- Expert paging to local NVMe
- LoRA adapter pipeline
- OpenAI-compatible server
- Streaming generation
- Throughput benchmarking

## Performance

Benchmark on Mac mini M4 Pro (24GB RAM):

| Model | Prefill | Decode | Memory |
|-------|---------|--------|--------|
| 8B    | 450 t/s | 22 t/s | 1.2GB  |
| 35B   | 120 t/s | 15 t/s | 2.8GB  |

## Development

Run tests:

```bash
cargo test --release
```
