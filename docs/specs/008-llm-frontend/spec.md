# 008 - Integración LLM en frontend (chat real)

## Objetivo

Mejorar la integración del chat del frontend con el LLM real, mostrando fuentes (RAG), manejo de errores, y una experiencia de conversación fluida.

## Historias

- Como usuario, quiero ver las fuentes (normativa) que el agente usó para responder.
- Como usuario, quiero ver un indicador de "escribiendo..." mientras el agente responde.
- Como usuario, quiero que se manejen los errores (timeout, rate limit) de forma clara.
- Como usuario, quiero que el chat recuerde el historial de la conversación.

## Criterios de aceptación

- [ ] El chat muestra las fuentes (RAG) en la respuesta del agente.
- [ ] El indicador de typing se muestra mientras espera respuesta.
- [ ] Los errores se manejan con mensajes claros.
- [ ] El historial de conversación se mantiene.
- [ ] Hay pruebas unitarias para el chat.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- Streaming de respuestas (V2).
- Multi-sesión (V2).