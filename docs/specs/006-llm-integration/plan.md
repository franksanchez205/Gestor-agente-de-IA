# Plan 006

## Stack

- LLM: OpenAI (gpt-4o) o Anthropic (claude-sonnet-4) — configurable por env.
- RAG: base de conocimiento con embeddings (OpenAI text-embedding-3-small) + vector store (pgvector o ChromaDB).
- Framework: LangChain o LlamaIndex (opcional).

## Componentes

- `src/agent/llm_client.py`: cliente unificado para OpenAI/Anthropic.
- `src/knowledge/vector_store.py`: vector store para RAG.
- `src/knowledge/ingest.py`: ingesta de normativa migratoria por país.
- Extender `ReasoningEngine` para usar el LLM real y el RAG real.

## Pruebas

- Unit: mock del LLM y del vector store.
- Integration: consulta real al LLM (con API key).
- E2E: flujo completo con respuesta del LLM real.