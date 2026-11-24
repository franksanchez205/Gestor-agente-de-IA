"""Cliente LLM unificado (OpenAI / Anthropic).

Permite elegir el proveedor por configuración (env LLM_PROVIDER).
"""

import os
from typing import Any


class LLMClient:
    def __init__(self, provider: str = "openai", model: str | None = None, api_key: str | None = None):
        self.provider = provider.lower()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("ANTHROPIC_API_KEY")
        if self.provider == "openai":
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
            import openai
            self._client = openai.AsyncOpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
            import anthropic
            self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

    async def complete(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
        if self.provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            resp = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content or ""
        else:
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system:
                kwargs["system"] = system
            resp = await self._client.messages.create(**kwargs)
            return resp.content[0].text if resp.content else ""