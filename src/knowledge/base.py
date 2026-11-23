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

    async def search(self, query: str, country: str | None = None, top_k: int = 5) -> list[str]:
        # Stub: búsqueda semántica en la base de normativa
        return []

    async def ingest(self, chunks: list[KnowledgeChunk]) -> None:
        # Stub: ingestar normativa actualizada
        pass