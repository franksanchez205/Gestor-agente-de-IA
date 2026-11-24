"""Tests de integración del ReasoningEngine con vector store y LLM mock."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.agent.reasoning import ReasoningEngine
from src.knowledge.base import KnowledgeBase
from src.knowledge.vector_store import InMemoryVectorStore
from src.knowledge.base import KnowledgeChunk


class FakeLLM:
    def __init__(self, response: str):
        self.response = response

    async def complete(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
        return self.response


@pytest.mark.asyncio
async def test_reasoning_with_rag_and_llm():
    store = InMemoryVectorStore()
    kb = KnowledgeBase(vector_store=store)
    await kb.ingest([
        KnowledgeChunk(country="AR", tramite="renovacion", source="Ley 25.871", content="Renovación de permiso de residencia: cada 2 años.", updated_at="2026-01-01"),
    ])
    llm = FakeLLM("Te ayudo a renovar tu permiso en Argentina.")
    engine = ReasoningEngine(llm_client=llm, knowledge_base=kb, system_prompt="Sos Puente.")

    result = await engine.understand("permiso", "Cliente: Juan", country="AR")
    assert "Argentina" in result.answer
    assert len(result.sources) == 1
    assert "Ley 25.871" in result.sources[0] or "Renovación" in result.sources[0]