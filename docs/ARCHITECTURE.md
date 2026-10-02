# Architecture

YAGBU follows a layered architecture so each platform can reuse the same model logic while implementing only the backend-specific execution layer.

## 1. Model layer

Responsible for:
- model family detection
- tokenizer metadata
- checkpoint path resolution
- adapter discovery and provenance

The model layer abstracts file layout and configuration so runtime code does not need to know whether a model is loaded from Hugging Face, local disk, or device storage.

## 2. Runtime layer

The runtime layer owns:
- generation loop
- token stream callbacks
- cache lifecycle
- routing / scheduling interface
- backend execution requests

This layer is where streaming and memory-aware inference logic is implemented.

## 3. Backend layer

Backends implement the execution contract of the runtime. Examples:
- Python / MLX backend for local Apple Silicon development
- native backend for Android and Windows
- Metal backend for iOS/macOS GPU paths
- CPU fallback backend for validation and debugging

## 4. Serving layer

The serving layer exposes:
- CLI tools
- HTTP endpoints
- chat session management
- prompt and context validation

## 5. App layer

The app layer is optional and platform-specific:
- Android app
- iOS app
- macOS desktop runtime
- Windows desktop runtime

The app layer should be thin and only handle UI, device integration, and command flow.

## Design principles

- backend isolation from model logic
- adapter-aware runtime
- low-memory expert offloading by default
- one shared API for local, server, and device use
- compatibility with Llama and OSS-style open models

## Target architecture

```text
User / Client
    |
    v
Serving layer
    |
    v
Runtime layer
    |
    +--> Model layer
    |
    +--> Backend layer (MLX / Metal / CPU / Native)
```
