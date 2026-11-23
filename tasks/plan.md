# Plan: Puente MVP

## Major components and dependencies

1. **Infraestructura base** (Docker, BD, Redis) — sin dependencias.
2. **Capa de datos** (modelos, migraciones, credenciales verificables) — depende de infraestructura.
3. **Núcleo del agente** (memoria, personalidad, orquestador, razonamiento) — depende de capa de datos.
4. **Capa de acción** (portales, pagos, citas) — depende de núcleo.
5. **Canal de interacción** (WhatsApp, voz, app) — depende de núcleo y capa de acción.
6. **Conocimiento** (normativa migratoria por país) — paralelo al núcleo.

## Implementation order

1. Infraestructura base + capa de datos.
2. Núcleo del agente (memoria + orquestador).
3. Conocimiento (RAG) + razonamiento (LLM).
4. Capa de acción (portales sandbox + pagos sandbox).
5. Canal (WhatsApp webhook + voz).
6. E2E + validación.

## Risks and mitigations

- **Sin API gubernamental**: usar RPA certificado o gestor humano como fallback.
- **Costos de LLM**: cachear respuestas frecuentes, usar modelos más baratos para tareas rutinarias.
- **Privacidad**: cifrado E2E desde el día 1, no agregar después.

## Parallel vs sequential

- Conocimiento (RAG) puede avanzar en paralelo con el núcleo.
- Canal puede avanzar en paralelo con la capa de acción (usando mocks).

## Verification checkpoints

- CP1: Infraestructura levanta y BD migra.
- CP2: Agente recuerda perfil y expediente (memoria personal).
- CP3: Agente responde consultas de normativa (RAG).
- CP4: Flujo completo en sandbox (trámite simulado).
- CP5: E2E pasa en staging.