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