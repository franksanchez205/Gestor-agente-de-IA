# Plan 004

## Datos

- Extender modelo `Document` para almacenar credenciales verificables (JWT-VC).
- Agregar modelo `Credential` (id, user_id, doc_id, vc_jwt, issued_at, expires_at, revoked).

## Agente

- Módulo de credenciales verificables (emisión, verificación, revocación).
- Integración con DID (self-sovereign identity).

## Capa de acción

- Verificador de credenciales (verifica firma y validez).
- Exportación/eliminación de datos del usuario.

## Pruebas

- Unit: emisión y verificación de VC, revocación, exportación.
- Integration: verificación cross-país (simulada).