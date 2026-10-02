from pathlib import Path

from yagbu.runtime import StreamingRuntime


def test_runtime_loads_fake_model(tmp_path):
    model_dir = tmp_path / "demo-llama"
    model_dir.mkdir()
    (model_dir / "config.json").write_text('{"model_type": "llama", "family": "llama"}', encoding="utf-8")

    runtime = StreamingRuntime(str(model_dir))
    assert runtime.model_spec.family == "llama"
    assert runtime.generate("hello", max_tokens=16).startswith("YAGBU response")


def test_runtime_chat_assembles_prompt(tmp_path):
    model_dir = tmp_path / "demo-qwen"
    model_dir.mkdir()
    (model_dir / "config.json").write_text('{"model_type": "qwen"}', encoding="utf-8")

    runtime = StreamingRuntime(str(model_dir))
    text = runtime.chat([
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
        {"role": "user", "content": "again"},
    ], max_tokens=32)
    assert "hello" in text and "again" in text
