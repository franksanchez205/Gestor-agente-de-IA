# Plan 002

## Datos

- Extender modelo `Case` para soportar múltiples trámites por usuario.
- Agregar modelo `Gestor` (id, nombre, país, especialidades, verificado, reputación, casos completados).
- Agregar modelo `Payment` (escrow para gestores).

## Agente

- Extender el orquestador para soportar múltiples planes activos por usuario.
- Extender el razonamiento (RAG) con normativa del segundo país.
- Extender la memoria personal para trackear trámites por país.

## Capa de acción

- Implementar marketplace de gestores (find_best, assign, release_payment).
- Extender portales para el segundo país.

## Canales

- WhatsApp y voz ya soportan multi-trámite (sin cambios).

## Pruebas

- Unit: marketplace de gestores, multi-trámite, segundo país.
- Integration: escrow de pagos.
- E2E: flujo completo en segundo país.