# Android YAGBU Runtime

## Overview

The Android YAGBU runtime brings efficient open-model inference to Android devices using the same architecture as the desktop version: expert offload, adapter pipelines, and budget-aware memory management.

## Platform specifics

- **Target**: Android 13+ (API 33)
- **Architecture**: arm64-v8a
- **Runtime**: Native C/C++ engine with JNI bindings (Kotlin app layer)
- **GPU**: Optional — CPU-first for deterministic numerics
- **Memory strategy**: SSD expert paging with UFS buffering

## Build

### Prerequisites

- JDK 17+
- Android SDK 35
- NDK r28 or later
- CMake 3.21+

### Build engine

```bash
cd android
bash tools/build_native.sh
```

This builds the native inference library and produces `.so` files for the app.

### Build app

```bash
./gradlew :app:assembleDebug
./gradlew :app:installDebug
```

## Models

Download models from Hugging Face and convert to GGUF format (same as desktop).

```bash
huggingface-cli download yagbu/yagbu-8b-preview --local-dir models/yagbu-8b
python ../tools/convert_to_gguf.py --dir models/yagbu-8b
```

Stage to device:

```bash
adb push models/yagbu-8b-gguf /sdcard/YAGBU/
```

## Architecture

```
Kotlin UI Layer
   |
   v
JNI Runtime Shell
   |
   v
Native Inference Engine (C/C++)
   |
   +-> Expert Manager (SSD paging)
   +-> Adapter Loader (LoRA / Recover)
   +-> Generation Loop (streaming tokens)
   +-> Memory Budget Tracker
```

## App features

- Model selection (8B / 35B / 70B when available)
- Chat interface with multi-turn context
- Temperature and top-p controls
- Real-time TTFT + throughput metrics
- Adapter warm/cold cache management

## Performance

Benchmark on Snapdragon 8 Elite (16 GB RAM):

| Model | TTFT (warm) | Decode | Memory |
|-------|-----------|--------|--------|
| 8B    | ~1.2s     | 18 t/s | ~500MB |
| 35B   | ~2.5s     | 9 t/s  | ~1.5GB |

## Testing

```bash
./gradlew :app:installDebugAndroidTest
adb shell am instrument -w dev.yagbu.runtime.app.test/androidx.test.runner.AndroidJUnitRunner
```
