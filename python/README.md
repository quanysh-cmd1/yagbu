# YAGBU Python package

This package is the reference implementation and the base for the full framework.

## Install

```bash
cd python
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Run

```bash
python -m yagbu
```

## Example

```python
from yagbu.runtime import StreamingRuntime

runtime = StreamingRuntime(model_dir="/path/to/model")
response = runtime.generate("Hello from YAGBU")
print(response)
```
