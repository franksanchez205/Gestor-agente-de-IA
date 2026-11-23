# Plan 000

## Infraestructura

- Docker Compose con PostgreSQL 16 (puerto 5432) y Redis 7 (puerto 6379).
- Variables de entorno en `.env` (DATABASE_URL, REDIS_URL, etc.).
- Eliminar atributo `version` obsoleto del compose.

## Backend

- FastAPI en `src/main.py`, puerto 8000.
- Ruta `GET /health` → `{"status": "ok"}`.
- Routers de WhatsApp y voz (stubs).
- Estructura de paquetes: src/agent, src/action, src/data, src/api, src/knowledge.

## Pruebas

- Backend: `tests/unit/test_memory.py` → memoria personal (agregar documento, vencimientos, contexto).
- Infra: verificación manual de PostgreSQL y Redis.

## Dependencias

- pyproject.toml con fastapi, uvicorn, sqlalchemy, alembic, redis, openai, anthropic, pytest, ruff.