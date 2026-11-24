"""Tests unitarios de la base de conocimiento (RAG multi-país)."""

import pytest
from src.knowledge.base import KnowledgeBase, KnowledgeChunk


class FakeStore:
    def __init__(self):
        self._docs = []

    def add(self, text, metadata=None):
        self._docs.append({"text": text, "metadata": metadata or {}})

    def search(self, query, top_k=5, country=None):
        results = []
        for doc in self._docs:
            if country and doc["metadata"].get("country") != country:
                continue
            if query.lower() in doc["text"].lower():
                results.append(doc["text"])
            if len(results) >= top_k:
                break
        return results


@pytest.mark.asyncio
async def test_ingest_registers_country():
    kb = KnowledgeBase(vector_store=FakeStore())
    await kb.ingest([KnowledgeChunk(country="AR", tramite="renovacion", source="ley", content="...", updated_at="2026-01-01")])
    assert "AR" in kb.countries
    assert await kb.has_country("AR") is True
    assert await kb.has_country("ES") is False


@pytest.mark.asyncio
async def test_ingest_multiple_countries():
    kb = KnowledgeBase(vector_store=FakeStore())
    await kb.ingest([
        KnowledgeChunk(country="AR", tramite="renovacion", source="ley", content="...", updated_at="2026-01-01"),
        KnowledgeChunk(country="ES", tramite="apostilla", source="ley", content="...", updated_at="2026-01-01"),
    ])
    assert set(kb.countries) == {"AR", "ES"}


@pytest.mark.asyncio
async def test_search_returns_list():
    kb = KnowledgeBase(vector_store=FakeStore())
    result = await kb.search("renovar permiso", country="AR")
    assert isinstance(result, list)