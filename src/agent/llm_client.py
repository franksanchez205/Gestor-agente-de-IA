"""Cliente LLM unificado (OpenAI / Anthropic).

Permite elegir el proveedor por configuración (env LLM_PROVIDER).
"""

import os
from typing import Any


class LLMClient:
    def __init__(self, provider: str = "openai", model: str | None = None, api_key: str | None = None):
        self.provider = provider.lower()
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        elif self.provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        elif self.provider == "gemini":
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        else:
            self.api_key = api_key
        if self.provider == "openai":
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            import openai
            self._client = openai.AsyncOpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
            import anthropic
            self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
        elif self.provider == "gemini":
            self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._genai = genai
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
        elif self.provider == "anthropic":
            kwargs: dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system:
                kwargs["system"] = system
            resp = await self._client.messages.create(**kwargs)
            return resp.content[0].text if resp.content else ""
        elif self.provider == "gemini":
            import asyncio
            model = self._genai.GenerativeModel(self.model)
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            # google-generativeai es sync; ejecutar en thread
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: model.generate_content(full_prompt))
            return resp.text if resp.text else ""
        else:
            raise ValueError(f"Proveedor no soportado: {self.provider}")