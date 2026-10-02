# YAGBU Python runtime guide

The Python package is the reference implementation for YAGBU and is the fastest path to local development and experimentation.

## Install

```bash
cd python
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Run the CLI

```bash
yagbu demo --model-dir ./models

yagbu chat "Explain the YAGBU runtime in one sentence." --model-dir ./models

yagbu serve --model-dir ./models --host 127.0.0.1 --port 8000
```

## Python API

```python
from yagbu.runtime import StreamingRuntime

runtime = StreamingRuntime(model_dir="./models")
print(runtime.generate("Hello from YAGBU", max_tokens=32))
print(runtime.chat([{"role": "user", "content": "Write a short hello message."}], max_tokens=16))
```

## Serve endpoint

The server exposes an OpenAI-compatible route at `/v1/chat/completions` and a health check at `/health`.
