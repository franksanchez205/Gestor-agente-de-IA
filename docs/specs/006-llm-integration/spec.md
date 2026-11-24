# 006 - Integración LLM real

## Objetivo

Conectar el agente Puente con un LLM real (OpenAI o Anthropic) y una base de conocimiento RAG con normativa migratoria real, reemplazando los stubs actuales.

## Historias

- Como usuario, quiero que el agente responda con información real sobre trámites migratorios.
- Como usuario, quiero que el agente cite la normativa aplicable.
- Como desarrollador, quiero poder elegir el proveedor de LLM (OpenAI/Anthropic).
- Como desarrollador, quiero que el RAG use una base de datos vectorial real.

## Criterios de aceptación

- [ ] El agente usa un LLM real para razonar y responder.
- [ ] El RAG consulta una base de conocimiento con normativa migratoria.
- [ ] Las respuestas incluyen citas de la normativa aplicable.
- [ ] El proveedor de LLM es configurable (OpenAI/Anthropic).
- [ ] Hay pruebas unitarias para la integración LLM y RAG.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- Fine-tuning del modelo (V2).
- Multi-idioma (V2).
- Caché de respuestas (V2).