"""Tests unitarios del cliente LLM unificado."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.agent.llm_client import LLMClient


@pytest.mark.asyncio
async def test_llm_client_openai_complete(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content="Respuesta OpenAI"))]
    with patch("openai.AsyncOpenAI") as mock_cls:
        instance = mock_cls.return_value
        instance.chat.completions.create = AsyncMock(return_value=mock_resp)
        client = LLMClient(provider="openai")
        result = await client.complete("Hola")
        assert result == "Respuesta OpenAI"


@pytest.mark.asyncio
async def test_llm_client_anthropic_complete(monkeypatch):
    try:
        import anthropic  # noqa: F401
    except ImportError:
        pytest.skip("anthropic no disponible (Windows Long Path)")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    mock_resp = MagicMock()
    mock_resp.content = [MagicMock(text="Respuesta Anthropic")]
    with patch("anthropic.AsyncAnthropic") as mock_cls:
        instance = mock_cls.return_value
        instance.messages.create = AsyncMock(return_value=mock_resp)
        client = LLMClient(provider="anthropic")
        result = await client.complete("Hola")
        assert result == "Respuesta Anthropic"


def test_llm_client_unsupported_provider():
    with pytest.raises(ValueError):
        LLMClient(provider="cohere")