# Plan 007

## Stack

- Auth: JWT (PyJWT) con access token y refresh token.
- Password hashing: bcrypt (passlib).
- Middleware: FastAPI dependency para validar JWT en endpoints protegidos.

## Componentes

- `src/auth/__init__.py`, `src/auth/jwt.py`, `src/auth/password.py`, `src/auth/deps.py`.
- `src/api/auth.py`: endpoints register, login, me.
- Extender `User` model con password_hash.
- Migración para agregar password_hash a users.

## Pruebas

- Unit: hashing, JWT encode/decode, dependency.
- Integration: register + login + acceso a endpoint protegido.
- E2E: flujo completo de auth.