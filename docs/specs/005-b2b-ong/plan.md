# Plan 005

## Datos

- Modelo `Organization` (id, name, type, contact_email, created_at).
- Modelo `Cupo` (id, org_id, beneficiary_email, assigned_at, used, used_at).
- Extender `User` con `org_id` (nullable) para vincular beneficiario a ONG.

## API

- `POST /api/orgs/register` — registrar ONG.
- `POST /api/orgs/{id}/cupos` — comprar/asignar cupos.
- `GET /api/orgs/{id}/report` — reporte de uso.
- `GET /api/cupos/{token}` — validar cupo de beneficiario.

## Frontend

- Panel de administración para ONG (dashboard con cupos y reportes).
- Flujo de activación para beneficiario (ingresar cupo).

## Pruebas

- Unit: gestión de cupos, asignación, reportes.
- Integration: flujo completo ONG → beneficiario.
- E2E: ONG compra cupos y beneficiario los usa.