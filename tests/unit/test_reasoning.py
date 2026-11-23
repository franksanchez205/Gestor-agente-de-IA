"""Tests unitarios del motor de razonamiento (LLM + RAG)."""

import pytest
from src.agent.reasoning import ReasoningEngine


class FakeLLM:
    def __init__(self, response: str):
        self.response = response
        self.last_prompt = None

    async def complete(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self.response


class FakeKB:
    def __init__(self, sources: list[str]):
        self.sources = sources
        self.last_query = None

    async def search(self, query: str) -> list[str]:
        self.last_query = query
        return self.sources


@pytest.mark.asyncio
async def test_understand_calls_kb_and_llm():
    llm = FakeLLM("Te ayudo a renovar tu permiso.")
    kb = FakeKB(["Ley de migraciones: renovación cada 2 años."])
    engine = ReasoningEngine(llm_client=llm, knowledge_base=kb)

    result = await engine.understand("Necesito renovar mi permiso", "Cliente: Juan")

    assert kb.last_query == "Necesito renovar mi permiso"
    assert "Juan" in llm.last_prompt
    assert "Ley de migraciones" in llm.last_prompt
    assert result.answer == "Te ayudo a renovar tu permiso."
    assert result.sources == ["Ley de migraciones: renovación cada 2 años."]


@pytest.mark.asyncio
async def test_understand_returns_sources():
    llm = FakeLLM("Respuesta")
    kb = FakeKB(["Fuente 1", "Fuente 2"])
    engine = ReasoningEngine(llm_client=llm, knowledge_base=kb)

    result = await engine.understand("consulta", "memoria")
    assert len(result.sources) == 2