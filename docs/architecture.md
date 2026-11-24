# Arquitectura

- /src: código fuente (Python, backend FastAPI)
  - /src/agent: núcleo del agente (memoria, personalidad, orquestador, razonamiento, notificaciones)
  - /src/action: capa de acción invisible (portales, gestores, pagos, citas)
  - /src/data: modelos, BD, credenciales verificables
  - /src/api: canales de interacción (WhatsApp, voz)
  - /src/knowledge: base de normativa migratoria por país (RAG)
  - /src/main.py: punto de entrada FastAPI (puerto 8000)
- /frontend: app web React + Vite + Tailwind (puerto 5173). Diseño distintivo estilo Jarvis.
- /docs/specs: specs numeradas (000-setup, 001-..., 002-..., 003-frontend)
- /tests: pruebas unitarias e integración
- Docker Compose: PostgreSQL (5433) + Redis (6379) + app (8000)
- El cliente solo habla con el agente (WhatsApp/voz/app). Portales, gestores y sistemas quedan invisibles detrás.
- El frontend llama a http://localhost:8000 (proxy en Vite).

## Estado de implementación (spec 001)

- [x] T1: Modelos de datos y migraciones (users, documents, cases).
- [x] T2: Memoria personal del agente.
- [x] T3: Orquestador de acciones.
- [x] T4: Motor de razonamiento (LLM + RAG).
- [x] T5: Capa de acción — portales.
- [x] T6: Capa de acción — pagos (sandbox).
- [x] T7: Canal WhatsApp (webhook).
- [x] T8: Canal voz (STT/TTS).
- [x] T9: Notificaciones proactivas.
- [x] T10: Tests E2E del flujo completo.
- [x] T11: Verificar criterios de aceptación.

Ver `docs/specs/001-tramite/tasks.md` para el detalle.

## Specs

- `docs/specs/000-setup/` — setup inicial (completada).
- `docs/specs/001-tramite/` — MVP trámite (completada).
- `docs/specs/002-tramites-expansion/` — V2: más trámites + segundo país (completada).
- `docs/specs/003-frontend/` — Frontend innovador estilo Jarvis (completada).
- `docs/specs/004-verifiable-credentials/` — Credenciales verificables transfronterizas (completada).