"""Motor de razonamiento del agente: LLM multimodal + RAG sobre normativa.

Entiende la intención del cliente, planifica pasos y consulta la base de
conocimiento de normativa migratoria por país antes de responder o actuar.
"""

from dataclasses import dataclass


@dataclass
class ReasoningResult:
    intent: str
    country: str | None
    tramite: str | None
    answer: str
    sources: list[str]
    needs_confirmation: bool = False


class ReasoningEngine:
    def __init__(self, llm_client, knowledge_base):
        self.llm = llm_client
        self.kb = knowledge_base

    async def understand(self, user_message: str, memory_context: str) -> ReasoningResult:
        # 1. Recuperar normativa relevante del RAG
        sources = await self.kb.search(user_message)
        # 2. Construir prompt con memoria + fuentes
        prompt = self._build_prompt(user_message, memory_context, sources)
        # 3. Llamar al LLM
        raw = await self.llm.complete(prompt)
        return self._parse(raw, sources)

    def _build_prompt(self, msg: str, memory: str, sources: list[str]) -> str:
        return (
            "Eres el agente personal de vida administrativa migratoria del cliente.\n"
            "Responde en lenguaje sencillo, sin jerga. Si el cliente pide realizar un "
            "trámite, planifica los pasos y pide confirmación antes de actuar.\n\n"
            f"MEMORIA DEL CLIENTE:\n{memory}\n\n"
            f"NORMATIVA RELEVANTE:\n{chr(10).join(sources)}\n\n"
            f"MENSAJE DEL CLIENTE:\n{msg}\n"
        )

    def _parse(self, raw: str, sources: list[str]) -> ReasoningResult:
        # Stub: en producción se parsea la respuesta estructurada del LLM
        return ReasoningResult(
            intent="unknown",
            country=None,
            tramite=None,
            answer=raw,
            sources=sources,
            needs_confirmation=False,
        )