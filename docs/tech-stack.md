# Stack

- Backend: Python 3.11+ + FastAPI
- Datos: PostgreSQL 16 + Redis 7
- Agente: LLM multimodal (OpenAI/Anthropic) + RAG (normativa migratoria por país)
- Documentos: W3C Verifiable Credentials (did-jwt-vc)
- Seguridad: cifrado E2E, OAuth2, auditoría de accesos
- Canales: WhatsApp Business API, voz (STT/TTS), app web (React, futuro)
- Infra: Docker Compose
- Pruebas: pytest + pytest-asyncio
- Lint: ruff

Versiones y dependencias detalladas en `pyproject.toml`.