# YAGBU roadmap

This roadmap turns the project from a concept into a working open-source framework in a controlled sequence.

## Phase 1: bootstrap and governance

Deliverables:
- repository structure
- contribution guide
- CI skeleton
- Python package metadata
- initial project docs

Goals:
- create a clean engineering foundation
- establish naming, coding conventions, and backlog structure

## Phase 2: model abstraction layer

Deliverables:
- model config parsing
- tier registry and family detection
- adapter contract for LoRA / pre-router / runtime state
- backend abstraction interface

Goals:
- make the runtime compatible with multiple model families and hardware targets
- avoid hardcoding one platform or one model architecture

## Phase 3: streaming inference engine

Deliverables:
- token generation loop
- streaming response API
- KV/cache management abstraction
- expert scheduling interface
- memory and paged-offload placeholders

Goals:
- run inference with low memory footprint and progressive output streaming
- establish the core engine primitives used by all platforms

## Phase 4: serving layer

Deliverables:
- CLI commands (`serve`, `chat`, `demo`)
- OpenAI-compatible request/response schema
- asynchronous handling and session state
- local HTTP server integration

Goals:
- enable developer testing and external service use from the same runtime

## Phase 5: platform ports

Deliverables:
- Python backend
- macOS runtime entry
- iOS runtime entry
- Android native integration
- Windows app/runtime pass-through

Goals:
- same model logic across devices with platform-specific optimized backends

## Phase 6: release quality and validation

Deliverables:
- benchmark harness
- model validation suite
- regression tests
- release notes and compatibility matrix

Goals:
- confidence in correctness, speed, and portability before public release

## Success metrics

- model config loads from a local directory
- chat generation works from a CLI and a Python API
- memory footprint is bounded and adapter reuse is supported
- cross-platform backend interfaces are stable
- benchmark output is collected and published

## Next milestone

The next milestone is to finalize the Python core: model config, runtime abstraction, generation loop, and local serving endpoint.
