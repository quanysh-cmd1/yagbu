# Windows YAGBU Runtime

## Overview

Desktop inference for Windows with CPU and GPU support. Runs open models on consumer hardware with efficient memory management.

## Platform specifics

- **Target**: Windows 10+
- **Processor**: x86-64 with AVX2+
- **GPU**: Optional Vulkan (AMD/Intel/NVIDIA)
- **Memory**: 8GB+ for 8B, 16GB+ for 35B
- **Storage**: Local SSD for expert paging

## Build and install

### Prerequisites

- Visual Studio 2022 or later
- CMake 3.21+
- Python 3.10+

### Build from source (C++)

```bash
cd windows
mkdir build && cd build
cmake ..
make
```

Binary at `bin/yagbu-windows.exe`.

## Usage

### Chat

```bash
yagbu-windows.exe chat --model-dir .\models\yagbu-8b
```

### Serve API

```bash
yagbu-windows.exe serve --model-dir .\models\yagbu-35b `
  --host 127.0.0.1 --port 8000
```

### Benchmark

```bash
yagbu-windows.exe bench --model-dir .\models\yagbu-8b
```

## Architecture

```
GUI / CLI
   |
   v
C++ Runtime
   |
   +-> CPU Inference (SIMD)
   +-> Vulkan GPU Backend (optional)
   +-> Expert Paging (NVMe)
   +-> Adapter Pipeline
```

## Features

- Multi-threaded CPU inference
- Optional Vulkan GPU acceleration
- Expert paging to NVMe
- LoRA adapter support
- OpenAI-compatible API
- Streaming generation
- Performance profiling

## Performance

Benchmark on Intel i7-13700K (32GB RAM) + RTX 3060:

| Model | Backend | Prefill | Decode |
|-------|---------|---------|--------|
| 8B    | CPU     | 150 t/s | 8 t/s  |
| 8B    | Vulkan  | 350 t/s | 18 t/s |
| 35B   | Vulkan  | 80 t/s  | 9 t/s  |

## Development

Run tests:

```bash
cmake --build . --target tests
ctest
```
