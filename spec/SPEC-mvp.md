# Spec: Puente MVP — V1

## Objective

Validar y construir el MVP de Puente: un agente de IA que gestiona un único trámite migratorio en un único país, actuando como único interlocutor del cliente. El cliente solo habla con el agente; el agente coordina todo lo demás (documentos, portales, pagos, citas) de forma invisible.

**Usuario objetivo**: migrante o familia transnacional en Latinoamérica que necesita renovar un permiso de residencia o apostillar/validar un título.

**Éxito**: el cliente completa el trámite hablando solo con el agente, con confirmación humana en puntos críticos, y el agente cobra solo si el trámite se completa.

## Tech Stack

- **Backend**: Python (FastAPI) + PostgreSQL + Redis
- **Agente**: LLM multimodal (OpenAI/Anthropic) + RAG (normativa migratoria)
- **Frontend/Canal**: WhatsApp Business API, voz (STT/TTS), app web (React)
- **Documentos**: W3C Verifiable Credentials (did-jwt-vc)
- **Seguridad**: cifrado E2E, OAuth2, auditoría de accesos

## Commands

```bash
# Dev
docker compose up -d
uvicorn app.main:app --reload

# Test
pytest --cov=app

# Lint
ruff check . && ruff format .

# Migrate DB
alembic upgrade head
```

## Project Structure

```
src/
  agent/        → Núcleo del agente (memoria, personalidad, orquestador, razonamiento)
  action/       → Capa de acción (portales, gestores, pagos, citas)
  data/         → Modelos, BD, credenciales verificables
  api/          → Endpoints REST (WhatsApp webhook, voz, app)
  knowledge/    → Base de normativa migratoria por país
tests/
  unit/
  integration/
  e2e/
spec/
  SPEC-mvp.md   → Este archivo
tasks/
  plan.md
  todo.md
```

## Code Style

- Python: PEP 8, type hints obligatorios, docstrings en funciones públicas.
- Nombres en inglés, código y comentarios en inglés.
- Un archivo por responsabilidad; máximo ~300 líneas por archivo.
- Tests junto al código (pytest).

## Testing Strategy

- **Unit**: lógica del agente, orquestador, validación de documentos.
- **Integration**: integración con portales (sandbox), pagos (sandbox), BD.
- **E2E**: flujo completo de un trámite (WhatsApp → agente → resultado).
- Cobertura mínima: 80% en `agent/` y `action/`.

## Boundaries

- **Always**: confirmación humana antes de enviar documentos, pagar o compartir datos; cifrado E2E; auditoría de accesos; tests antes de commit.
- **Ask first**: cambiar de país/trámite MVP; sumar un gestor nuevo; cambiar nivel de autonomía del agente.
- **Never**: dar asesoría jurídica vinculante; vender datos de usuarios; actuar sin confirmación en puntos críticos; recibir documentos sin cifrado E2E.

## Success Criteria

- Un cliente completa el trámite hablando solo con el agente (WhatsApp o voz).
- El agente confirma antes de enviar/pagar.
- El expediente se actualiza con credenciales verificables.
- El cliente recibe notificaciones proactivas (ej. 60 días antes de vencimiento).
- Cobertura de tests ≥ 80% en `agent/` y `action/`.
- Flujo E2E pasa en entorno de staging.

## Out of Scope (Deferred)

- Multi-país simultáneo (V2).
- Multi-trámite simultáneo (V2).
- Marketplace de gestores maduro (V2).
- Credenciales verificables transfronterizas completas (V3).
- B2B (ONG/organismos) (V3).

## Open Questions

- ¿Qué país y trámite elegir para el MVP?
- ¿Qué LLM usar (OpenAI vs Anthropic) y con qué costos?
- ¿Qué portal gubernamental tiene API disponible para el MVP?