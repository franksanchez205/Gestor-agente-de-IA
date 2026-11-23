# Tareas: Puente MVP

- [x] T1: Inicializar proyecto (estructura de carpetas, Docker, pyproject.toml)
  - Acceptance: `docker compose up` levanta BD y Redis sin errores
  - Verify: `docker compose ps` muestra servicios healthy
  - Files: docker-compose.yml, pyproject.toml, .env.example

- [ ] T2: Modelos de datos y migraciones (usuario, expediente, trámite, credencial)
  - Acceptance: migración crea tablas y se puede crear un usuario
  - Verify: `alembic upgrade head` sin errores; test de creación de usuario pasa
  - Files: src/data/models.py, src/data/migrations/

- [ ] T3: Memoria personal del agente (perfil, expediente, historial, preferencias)
  - Acceptance: el agente recuerda datos del cliente entre sesiones
  - Verify: test unitario de memoria personal pasa
  - Files: src/agent/memory.py

- [ ] T4: Orquestador de acciones (plan de trámite, confirmaciones)
  - Acceptance: orquestador genera plan y pide confirmación en puntos críticos
  - Verify: test unitario del orquestador pasa
  - Files: src/agent/orchestrator.py

- [ ] T5: Motor de razonamiento (LLM + RAG normativa migratoria)
  - Acceptance: agente responde consultas de normativa con fuentes
  - Verify: test de RAG pasa; respuesta incluye cita de norma
  - Files: src/agent/reasoning.py, src/knowledge/

- [ ] T6: Capa de acción — portales (sandbox)
  - Acceptance: agente puede enviar formulario a portal sandbox
  - Verify: test de integración con portal sandbox pasa
  - Files: src/action/portals.py

- [ ] T7: Capa de acción — pagos (sandbox)
  - Acceptance: agente puede pagar tasa en sandbox con confirmación
  - Verify: test de integración con pago sandbox pasa
  - Files: src/action/payments.py

- [ ] T8: Canal WhatsApp (webhook + envío de mensajes)
  - Acceptance: cliente envía mensaje y recibe respuesta del agente
  - Verify: test E2E de WhatsApp webhook pasa
  - Files: src/api/whatsapp.py

- [ ] T9: Canal voz (STT/TTS)
  - Acceptance: cliente habla y el agente responde por voz
  - Verify: test de voz pasa
  - Files: src/api/voice.py

- [ ] T10: Notificaciones proactivas (vencimientos, cambios normativos)
  - Acceptance: agente envía aviso 60 días antes de vencimiento
  - Verify: test de notificación programada pasa
  - Files: src/agent/notifications.py

- [ ] T11: Tests E2E del flujo completo
  - Acceptance: flujo completo (WhatsApp → agente → resultado) pasa en staging
  - Verify: `pytest tests/e2e/` pasa
  - Files: tests/e2e/

- [ ] T12: Documentación y README final
  - Acceptance: README describe cómo levantar y probar
  - Verify: revisión manual
  - Files: README.md