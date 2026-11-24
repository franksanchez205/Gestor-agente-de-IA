"""Tests de integración con LLM real (requiere API key)."""

import os
import pytest

OPENAI_KEY = os.getenv("OPENAI_API_KEY")


@pytest.mark.skipif(not OPENAI_KEY, reason="OPENAI_API_KEY no configurada")
@pytest.mark.asyncio
async def test_llm_real_complete():
    from src.agent.llm_client import LLMClient
    client = LLMClient(provider="openai")
    result = await client.complete("Responde solo: OK")
    assert isinstance(result, str)
    assert len(result) > 0