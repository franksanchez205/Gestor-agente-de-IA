"""API de chat con el agente (integración LLM real)."""

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agent.reasoning import ReasoningEngine
from src.knowledge.base import KnowledgeBase
from src.knowledge.vector_store import InMemoryVectorStore

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory knowledge base (stub; en producción se usa pgvector)
_store = InMemoryVectorStore()
_kb = KnowledgeBase(vector_store=_store)

# Ingestar normativa de ejemplo para RAG
from src.knowledge.base import KnowledgeChunk

_kb_ingest_task = None
try:
    import asyncio

    async def _ingest():
        await _kb.ingest([
            KnowledgeChunk(country="AR", tramite="renovacion", source="Ley 25.871", content="Renovación de permiso de residencia en Argentina: se debe solicitar 60 días antes del vencimiento. Requiere DNI, comprobante de domicilio y foto.", updated_at="2026-01-01"),
            KnowledgeChunk(country="AR", tramite="apostilla", source="Convención de La Haya", content="Apostilla de documentos en Argentina: se tramita ante el Ministerio de Relaciones Exteriores. Valida para países firmantes de la Convención de La Haya.", updated_at="2026-01-01"),
            KnowledgeChunk(country="ES", tramite="apostilla", source="Convención de La Haya", content="Apostilla de título universitario en España: se tramita ante el Ministerio de Justicia. El título debe estar previamente legalizado en el país de origen.", updated_at="2026-01-01"),
            KnowledgeChunk(country="ES", tramite="residencia", source="Ley de Extranjería", content="Permiso de residencia en España: renovación cada 2 años. Requiere pasaporte vigente, seguro médico y medios económicos.", updated_at="2026-01-01"),
        ])

    # Ejecutar ingesta al importar el módulo
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(_ingest())
    else:
        loop.run_until_complete(_ingest())
except Exception:
    pass


class ChatRequest(BaseModel):
    message: str
    country: str | None = "AR"


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


@router.post("/")
async def chat(req: ChatRequest):
    # Intentar usar LLM real si hay API key
    # Seleccionar proveedor disponible
    if os.getenv("OPENAI_API_KEY"):
        from src.agent.llm_client import LLMClient
        llm = LLMClient(provider="openai")
    elif os.getenv("ANTHROPIC_API_KEY"):
        from src.agent.llm_client import LLMClient
        llm = LLMClient(provider="anthropic")
    elif os.getenv("GEMINI_API_KEY"):
        from src.agent.llm_client import LLMClient
        llm = LLMClient(provider="gemini")
    else:
        # Mock LLM para desarrollo sin API key
        class MockLLM:
            async def complete(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
                return "Recibí tu solicitud. Estoy preparando el plan del trámite; te confirmo antes de enviar cualquier cosa. ¿Autorizás que gestione por vos?"

        llm = MockLLM()

    engine = ReasoningEngine(llm_client=llm, knowledge_base=_kb)
    try:
        result = await engine.understand(req.message, memory_context="Cliente: Juan", country=req.country)
        return ChatResponse(answer=result.answer, sources=result.sources)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))