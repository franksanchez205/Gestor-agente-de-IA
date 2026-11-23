# Arquitectura

- /src: código fuente (Python)
  - /src/agent: núcleo del agente (memoria, personalidad, orquestador, razonamiento, notificaciones)
  - /src/action: capa de acción invisible (portales, gestores, pagos, citas)
  - /src/data: modelos, BD, credenciales verificables
  - /src/api: canales de interacción (WhatsApp, voz)
  - /src/knowledge: base de normativa migratoria por país (RAG)
  - /src/main.py: punto de entrada FastAPI (puerto 8000)
- /docs/specs: specs numeradas (000-setup, 001-..., ...)
- /tests: pruebas unitarias e integración
- Docker Compose: PostgreSQL (5432) + Redis (6379) + app (8000)
- El cliente solo habla con el agente (WhatsApp/voz/app). Portales, gestores y sistemas quedan invisibles detrás.
- El frontend (futuro) llama a http://localhost:8000/api (CORS habilitado).

## Estado de implementación (spec 001)

- [x] T1: Modelos de datos y migraciones (users, documents, cases).
- [x] T2: Memoria personal del agente.
- [x] T3: Orquestador de acciones.
- [x] T4: Motor de razonamiento (LLM + RAG).
- [x] T5: Capa de acción — portales.
- [ ] T6: Capa de acción — pagos (sandbox).
- [ ] T7: Canal WhatsApp (webhook).
- [ ] T8: Canal voz (STT/TTS).
- [ ] T9: Notificaciones proactivas.
- [ ] T10: Tests E2E.
- [ ] T11: Verificar criterios de aceptación.

Ver `docs/specs/001-tramite/tasks.md` para el detalle.