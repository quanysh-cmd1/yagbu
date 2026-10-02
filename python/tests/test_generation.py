from pathlib import Path

from yagbu.adapters import AdapterManager
from yagbu.generation import GenerationConfig, GenerationSession
from yagbu.offload import ExpertOffloadStrategy, MemoryBudget, OffloadPolicy, SSDPageManager


def test_adapter_discovery(tmp_path):
    """Test that adapters are discovered in model directory."""
    model_dir = tmp_path / "test-model"
    model_dir.mkdir()

    # Create fake adapter files
    (model_dir / "lora_test.safetensors").touch()
    (model_dir / "prerouter_test.safetensors").touch()
    (model_dir / "recover_style.safetensors").touch()

    manager = AdapterManager(str(model_dir))
    adapters = manager.list_adapters()
    assert "lora_test" in adapters
    assert "prerouter_test" in adapters
    assert "recover_style" in adapters


def test_adapter_get_by_type(tmp_path):
    """Test adapter filtering by type."""
    model_dir = tmp_path / "test-model"
    model_dir.mkdir()

    (model_dir / "lora_a.safetensors").touch()
    (model_dir / "lora_b.safetensors").touch()
    (model_dir / "prerouter_x.safetensors").touch()

    manager = AdapterManager(str(model_dir))
    loras = manager.get_by_type("lora")
    assert len(loras) == 2

    prerouters = manager.get_by_type("prerouter")
    assert len(prerouters) == 1


def test_adapter_has_adapters(tmp_path):
    """Test adapter presence detection."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    manager_empty = AdapterManager(str(empty_dir))
    assert not manager_empty.has_adapters()

    with_adapters = tmp_path / "with-adapters"
    with_adapters.mkdir()
    (with_adapters / "lora_test.safetensors").touch()
    manager_full = AdapterManager(str(with_adapters))
    assert manager_full.has_adapters()


def test_memory_budget_tracking():
    """Test memory budget calculation."""
    budget = MemoryBudget(total_available_mb=2048)
    assert budget.available_mb() == 2048
    assert budget.used_mb() == 0

    budget.resident_experts_mb = 512
    budget.kv_cache_mb = 256
    assert budget.used_mb() == 768
    assert budget.available_mb() == 1280
    assert budget.is_within_budget(1280)
    assert not budget.is_within_budget(1281)


def test_ssd_page_manager_warm_cache():
    """Test expert warm/cold cache tracking."""
    manager = SSDPageManager()
    assert not manager.is_warm(0, 0)

    manager.mark_warm(0, 0)
    assert manager.is_warm(0, 0)

    manager.schedule_expert_page_in(1, 0)
    requests = manager.get_page_requests()
    assert (0, 1) in requests
    assert len(manager.get_page_requests()) == 0  # Requests cleared


def test_expert_offload_strategy_prediction():
    """Test expert routing prediction."""
    strategy = ExpertOffloadStrategy(
        num_experts_per_layer=256,
        num_active_experts=8,
        model_family="llama",
    )

    predicted = strategy.predict_expert_selection(token_position=0, layer=0)
    assert len(predicted) <= 8
    assert all(0 <= idx < 256 for idx in predicted)

    # Same input should give deterministic output
    predicted2 = strategy.predict_expert_selection(token_position=0, layer=0)
    assert predicted == predicted2


def test_generation_session_lifecycle(tmp_path):
    """Test full generation session workflow."""
    model_dir = tmp_path / "test-model"
    model_dir.mkdir()
    (model_dir / "config.json").write_text('{"model_type": "llama"}', encoding="utf-8")

    session = GenerationSession(str(model_dir), model_family="llama")
    assert session.memory_budget.available_mb() == 2048
    assert session.session_state["prefill_done"] is False

    # Prefill a prompt
    session.prefill_prompt([1, 2, 3, 4, 5])
    assert session.session_state["prefill_done"] is True
    assert session.session_state["token_count"] == 5

    # Generate tokens
    config = GenerationConfig(max_tokens=10, stream=True)
    stream = session.generate_tokens(num_tokens=10, config=config)
    tokens = list(stream)
    assert len(tokens) == 10
    assert all(isinstance(t, str) for t in tokens)

    # Check memory status
    status = session.get_memory_status()
    assert status["total_available_mb"] == 2048
    assert status["available_mb"] >= 0

    session.close()
    assert len(session.session_state) == 0


def test_generation_session_adapter_loading(tmp_path):
    """Test adapter loading within a session."""
    model_dir = tmp_path / "test-model"
    model_dir.mkdir()
    (model_dir / "lora_model.safetensors").touch()
    (model_dir / "prerouter_model.safetensors").touch()

    session = GenerationSession(str(model_dir), model_family="llama")
    session.load_adapters()
    assert "lora_model" in session.session_state["active_adapters"]
    assert "prerouter_model" in session.session_state["active_adapters"]


def test_token_stream_iterator():
    """Test TokenStream as iterator."""
    tokens = ["hello", "world", "from", "yagbu"]
    stream = TokenStream(tokens, metadata={"model": "test"})

    assert stream.has_more()
    result = list(stream)
    assert result == tokens
    assert not stream.has_more()


def test_generation_config_defaults():
    """Test GenerationConfig with default values."""
    config = GenerationConfig()
    assert config.max_tokens == 128
    assert config.temperature == 0.7
    assert config.top_p == 0.9
    assert config.stream is True
    assert config.stop_sequences == []
