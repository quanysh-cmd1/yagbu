from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .runtime import StreamingRuntime


def _build_runtime(model_dir: str) -> StreamingRuntime:
    return StreamingRuntime(model_dir=model_dir)


def demo_command(model_dir: str) -> None:
    runtime = _build_runtime(model_dir)
    print(runtime.generate("Hello from YAGBU demo", max_tokens=32))


def chat_command(model_dir: str, prompt: str) -> None:
    runtime = _build_runtime(model_dir)
    print(runtime.chat([{"role": "user", "content": prompt}], max_tokens=64))


def serve_command(model_dir: str, host: str = "127.0.0.1", port: int = 8000) -> None:
    try:
        import uvicorn
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("Please install YAGBU serve extras: pip install 'yagbu[serve]'") from exc

    from .server import create_app

    app = create_app(lambda: _build_runtime(model_dir))
    uvicorn.run(app, host=host, port=port)


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="yagbu", description="YAGBU local inference CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="create a demo generation")
    demo.add_argument("--model-dir", default="./models", help="Path to a local model directory")

    chat = subparsers.add_parser("chat", help="run a one-shot chat prompt")
    chat.add_argument("prompt", help="Input text prompt")
    chat.add_argument("--model-dir", default="./models", help="Path to a local model directory")

    serve = subparsers.add_parser("serve", help="serve a local OpenAI-compatible API")
    serve.add_argument("--model-dir", default="./models", help="Path to a local model directory")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "demo":
        demo_command(args.model_dir)
    elif args.command == "chat":
        chat_command(args.model_dir, args.prompt)
    elif args.command == "serve":
        serve_command(args.model_dir, host=args.host, port=args.port)
    else:
        parser.error("Unsupported command")


if __name__ == "__main__":
    main()
