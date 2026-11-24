"""Base de conocimiento: normativa migratoria por país (RAG)."""

from dataclasses import dataclass


@dataclass
class KnowledgeChunk:
    country: str
    tramite: str
    source: str  # ley, decreto, resolución
    content: str
    updated_at: str


class KnowledgeBase:
    def __init__(self, vector_store):
        self.store = vector_store
        self._countries: set[str] = set()

    @property
    def countries(self) -> list[str]:
        return sorted(self._countries)

    async def search(self, query: str, country: str | None = None, top_k: int = 5) -> list[str]:
        return self.store.search(query, top_k=top_k, country=country)

    async def ingest(self, chunks: list[KnowledgeChunk]) -> None:
        from src.knowledge.ingest import ingest_normativa
        ingest_normativa(self.store, chunks)
        for chunk in chunks:
            self._countries.add(chunk.country)

    async def has_country(self, country: str) -> bool:
        return country in self._countries