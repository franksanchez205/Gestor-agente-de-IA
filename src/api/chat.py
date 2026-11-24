"""API de chat con el agente (integración LLM real)."""

import os
from fastapi import APIRouter
from pydantic import BaseModel

from src.agent.reasoning import ReasoningEngine
from src.knowledge.base import KnowledgeBase
from src.knowledge.vector_store import InMemoryVectorStore

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory knowledge base (stub; en producción se usa pgvector)
_store = InMemoryVectorStore()
_kb = KnowledgeBase(vector_store=_store)


class ChatRequest(BaseModel):
    message: str
    country: str | None = "AR"


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


@router.post("/")
async def chat(req: ChatRequest):
    # Intentar usar LLM real si hay API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        from src.agent.llm_client import LLMClient
        llm = LLMClient(provider="openai")
    else:
        # Mock LLM para desarrollo sin API key
        class MockLLM:
            async def complete(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
                return "Recibí tu solicitud. Estoy preparando el plan del trámite; te confirmo antes de enviar cualquier cosa. ¿Autorizás que gestione por vos?"

        llm = MockLLM()

    engine = ReasoningEngine(llm_client=llm, knowledge_base=_kb)
    result = await engine.understand(req.message, memory_context="Cliente: Juan", country=req.country)
    return ChatResponse(answer=result.answer, sources=result.sources)