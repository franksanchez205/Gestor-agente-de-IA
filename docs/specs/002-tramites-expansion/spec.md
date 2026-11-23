# 002 - Expansión: más trámites + segundo país

## Objetivo

Ampliar el MVP (spec 001) para soportar 2-3 trámites adicionales en el país inicial y agregar un segundo país, con marketplace de gestores verificados básico.

## Historias

- Como usuario, quiero gestionar varios trámites (no solo uno) con el mismo agente.
- Como usuario, quiero gestionar trámites en un segundo país (ej. apostilla de título para España).
- Como usuario, quiero que el agente seleccione un gestor verificado cuando el trámite lo requiera.
- Como gestor, quiero recibir casos con todo el contexto y cobrar por escrow al completar.

## Criterios de aceptación

- [ ] El agente soporta al menos 3 trámites en el país inicial (ej. renovación de permiso, apostilla, validación de título).
- [ ] El agente soporta al menos 1 trámite en un segundo país.
- [ ] El agente selecciona un gestor verificado para trámites que lo requieran.
- [ ] El pago al gestor se libera por escrow al completar el trámite.
- [ ] Hay pruebas unitarias para el marketplace y la expansión multi-trámite.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- Credenciales verificables transfronterizas completas (spec 003).
- B2B (ONG/organismos) (spec 004).
- Multi-país simultáneo (más de 2 países) (spec 004).
- Asesoría jurídica vinculante (nunca).