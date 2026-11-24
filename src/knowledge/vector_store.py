"""Vector store para RAG (in-memory por defecto, extensible a pgvector/ChromaDB)."""

from typing import Any


class InMemoryVectorStore:
    def __init__(self):
        self._docs: list[dict[str, Any]] = []

    def add(self, text: str, metadata: dict[str, Any] | None = None) -> None:
        self._docs.append({"text": text, "metadata": metadata or {}})

    def search(self, query: str, top_k: int = 5, country: str | None = None) -> list[str]:
        # Stub: búsqueda por substring (en producción se usa similitud de embeddings)
        results = []
        for doc in self._docs:
            if country and doc["metadata"].get("country") != country:
                continue
            if query.lower() in doc["text"].lower():
                results.append(doc["text"])
            if len(results) >= top_k:
                break
        return results

    def count(self) -> int:
        return len(self._docs)