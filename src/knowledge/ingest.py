"""Ingesta de normativa migratoria por país en el vector store."""

from src.knowledge.base import KnowledgeChunk
from src.knowledge.vector_store import InMemoryVectorStore


def ingest_normativa(store: InMemoryVectorStore, chunks: list[KnowledgeChunk]) -> int:
    """Ingesta chunks de normativa en el vector store.

    Returns:
        Número de chunks ingestados.
    """
    for chunk in chunks:
        store.add(
            text=chunk.content,
            metadata={
                "country": chunk.country,
                "tramite": chunk.tramite,
                "source": chunk.source,
                "updated_at": chunk.updated_at,
            },
        )
    return len(chunks)