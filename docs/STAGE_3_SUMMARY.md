# YAGBU Stage 3: SSD/Offload + Adapter + Generation

This stage completes the core runtime architecture with realistic expert offload, adapter management, and streaming generation.

## What's new in Stage 3

### 1. Adapter Pipeline
- `adapters.py`: Model adapter discovery and lifecycle
- Support for LoRA, Recover-style, and prerouter adapters
- Automatic adapter file scanning in model directory
- Per-adapter metadata and tracking

### 2. Offload & Memory
- `offload.py`: SSD expert paging abstraction
- Memory budget tracking and allocation
- Expert warm/cold cache management
- Prefetch scheduling interface
- Multiple offload policies: RESIDENT, SSD_DEMAND, HYBRID, STREAMING

### 3. Generation Loop
- `generation.py`: Full session-based generation
- TokenStream for streaming output
- GenerationSession with multi-turn state
- Position-based expert prefetching
- Memory status tracking

### 4. Platform Starter Docs
- Android: native engine + JNI, Kotlin app, expert paging via UFS
- iOS: Metal + MLX Swift, on-device chat, expert repacking
- macOS: Rust runtime wrapper, Python backend via FFI
- Windows: C++ core, optional Vulkan, CPU SIMD

## Architecture flow

```
User Request
   |
   v
StreamingRuntime (Python layer)
   |
   +--> GenerationSession
   |      |
   |      +--> AdapterManager (load LoRA, prerouter, recover)
   |      +--> ExpertOffloadStrategy (prefetch, schedule)
   |      +--> GenerationConfig (temp, top_p, max_tokens)
   |
   +--> TokenStream (yield tokens)
       |
       v
   Response (CLI / API / App)
```

## Key interfaces

### AdapterManager
```python
manager = AdapterManager(model_dir)
adapters = manager.list_adapters()  # Find all adapters
manager.load_adapters(["lora_model", "prerouter_model"])
spec = manager.get_adapter("lora_model")
```

### ExpertOffloadStrategy
```python
strategy = ExpertOffloadStrategy(num_experts_per_layer=256, num_active_experts=8)
predicted = strategy.predict_expert_selection(token_pos=0, layer=0)
strategy.schedule_prefetch(token_pos=1, layer=0)
```

### GenerationSession
```python
session = GenerationSession(model_dir, model_family="llama")
session.load_adapters(["lora_model"])
session.prefill_prompt([1, 2, 3, 4, 5])
stream = session.generate_tokens(num_tokens=64)
for token in stream:
    print(token, end="")
session.close()
```

## Testing

```bash
cd python
pytest tests/test_generation.py -v
```

## Test coverage

- Adapter discovery and filtering
- Memory budget tracking
- Expert warm/cold cache
- Expert prediction and prefetch
- Generation session lifecycle
- Adapter loading in session
- TokenStream iteration
- Generation config defaults

## Next steps (Stage 4)

- Full inference backend integration (MLX / CUDA / Metal)
- Real tokenizer and model weight loading
- Streaming HTTP endpoints with proper error handling
- Benchmark harness and throughput profiling
- Model family-specific configs (Llama, Qwen, Mistral)

## Status

YAGBU is now a realistic prototype with:
- ✅ model abstraction
- ✅ adapter-aware runtime
- ✅ expert offload scheduling
- ✅ streaming generation
- ✅ cross-platform starter docs
- ✅ comprehensive pytest suite
- 🔧 backend implementations (coming in Stage 4)
