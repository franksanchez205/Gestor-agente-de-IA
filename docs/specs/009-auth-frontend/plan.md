# Plan 009

## Componentes

- Frontend: `src/auth.ts` (helpers para token), `src/LoginForm.tsx`, `src/RegisterForm.tsx`.
- Frontend: modificar `App.tsx` para mostrar login/register si no hay token.
- Frontend: agregar header de usuario con logout.

## Pruebas

- Unit: auth helpers (save/load/clear token).
- E2E: flujo de registro + login + acceso protegido.