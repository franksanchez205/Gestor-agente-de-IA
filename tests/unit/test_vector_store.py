"""Tests unitarios del vector store para RAG."""

import pytest
from src.knowledge.vector_store import InMemoryVectorStore


def test_add_and_count():
    store = InMemoryVectorStore()
    store.add("Normativa de residencia en Argentina", metadata={"country": "AR"})
    assert store.count() == 1


def test_search_by_substring():
    store = InMemoryVectorStore()
    store.add("Renovar permiso de residencia en Argentina", metadata={"country": "AR"})
    store.add("Apostillar título en España", metadata={"country": "ES"})
    results = store.search("permiso", country="AR")
    assert len(results) == 1
    assert "Argentina" in results[0]


def test_search_filters_by_country():
    store = InMemoryVectorStore()
    store.add("Normativa AR", metadata={"country": "AR"})
    store.add("Normativa ES", metadata={"country": "ES"})
    results = store.search("Normativa", country="ES")
    assert len(results) == 1
    assert "ES" in results[0]