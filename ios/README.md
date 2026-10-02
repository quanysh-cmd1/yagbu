# iOS YAGBU Runtime

## Overview

On-device chat inference for iPhone and iPad. Efficient open-model inference using Metal for GPU compute and native Swift runtime.

## Platform specifics

- **Target**: iOS 17+
- **Device**: Apple Silicon (A14+), recommended A17 Pro or M-series
- **GPU**: Metal with MLX Swift backend
- **Memory**: 8GB+ for 8B, 12GB+ for 35B with expert paging

## Build

### Prerequisites

- macOS 13+
- Xcode 15+
- Python 3.10+ (for model conversion)

### Download models

```bash
python3 -m venv .venv-tools
.venv-tools/bin/pip install huggingface_hub numpy

# 8B model (direct)
.venv-tools/bin/huggingface-cli download yagbu/yagbu-8b-preview \
  --local-dir Models/yagbu-8b

# 35B model (requires repacking for iPhone storage layout)
mkdir -p checkpoints
.venv-tools/bin/huggingface-cli download yagbu/yagbu-35b-preview \
  --local-dir checkpoints/yagbu-35b

python tools/repack_experts.py pack checkpoints/yagbu-35b Models/yagbu-35b
python tools/repack_experts.py verify checkpoints/yagbu-35b Models/yagbu-35b
```

### Build app

```bash
xcodebuild -project YAGBU.xcodeproj \
  -scheme YAGBUPhone \
  -destination generic/platform=iOS \
  build
```

## Architecture

```
SwiftUI Chat Screen
   |
   v
YAGBUViewModel + async/await
   |
   v
MLX Swift Inference Layer
   |
   +-> Model Loading (resident + expert files)
   +-> Adapter Pipeline (LoRA + Prerouter)
   +-> Token Generation (streaming)
   +-> Memory Management (SSD expert paging)
```

## Features

- Chat interface with system prompt control
- Model selection (8B / 35B)
- Temperature and generation controls
- Real-time token-per-second metrics
- Multi-turn context with efficient KV caching

## Performance

Benchmark on iPhone 16 Pro (8GB RAM):

| Model | TTFT | Decode | Memory |
|-------|------|--------|--------|
| 8B    | 1.8s | 12 t/s | 400MB  |
| 35B   | 3.2s | 6 t/s  | 1.2GB  |

## Testing

```bash
xcodebuild -project YAGBU.xcodeproj \
  -scheme YAGBUPhoneTests \
  test
```
