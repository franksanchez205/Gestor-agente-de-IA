"""Tests E2E con respuesta real del LLM (requiere API key)."""

import os
import pytest

OPENAI_KEY = os.getenv("OPENAI_API_KEY")


@pytest.mark.skipif(not OPENAI_KEY, reason="OPENAI_API_KEY no configurada")
@pytest.mark.asyncio
async def test_llm_flow_end_to_end():
    from src.agent.llm_client import LLMClient
    from src.knowledge.base import KnowledgeBase
    from src.knowledge.vector_store import InMemoryVectorStore
    from src.knowledge.base import KnowledgeChunk
    from src.agent.reasoning import ReasoningEngine

    store = InMemoryVectorStore()
    kb = KnowledgeBase(vector_store=store)
    await kb.ingest([
        KnowledgeChunk(country="AR", tramite="renovacion", source="Ley 25.871", content="Renovación de permiso de residencia en Argentina: cada 2 años.", updated_at="2026-01-01"),
    ])
    llm = LLMClient(provider="openai")
    engine = ReasoningEngine(llm_client=llm, knowledge_base=kb)
    result = await engine.understand("permiso", "Cliente: Juan", country="AR")
    assert isinstance(result.answer, str)
    assert len(result.answer) > 0
    assert len(result.sources) >= 1