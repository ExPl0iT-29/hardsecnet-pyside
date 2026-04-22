from __future__ import annotations

from hardsecnet_pyside.agents import AgentEngine
from hardsecnet_pyside.config import AISettings


def test_ai_settings_live_ollama_env(monkeypatch) -> None:
    monkeypatch.setenv("HARDSECNET_OLLAMA_LIVE", "1")
    monkeypatch.setenv("HARDSECNET_AI_TIMEOUT_SECONDS", "2.5")

    settings = AISettings.from_env()

    assert settings.live_enabled is True
    assert settings.request_timeout_seconds == 2.5


def test_agent_engine_uses_deterministic_fallback_when_live_disabled() -> None:
    engine = AgentEngine(AISettings(live_enabled=False))

    text, runtime, error = engine._generate_text("prompt", "fallback explanation")

    assert text == "fallback explanation"
    assert runtime == "deterministic_fallback"
    assert error == ""
