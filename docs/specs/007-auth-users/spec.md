# 007 - Autenticación y usuarios

## Objetivo

Implementar un sistema de autenticación (OAuth/JWT) y gestión de usuarios reales, reemplazando los stubs actuales donde el usuario se identifica por ID fijo.

## Historias

- Como usuario, quiero registrarme con email y contraseña.
- Como usuario, quiero iniciar sesión y obtener un token JWT.
- Como usuario, quiero que mis datos (expediente, trámites) estén protegidos y solo accesibles por mí.
- Como administrador, quiero gestionar usuarios.

## Criterios de aceptación

- [ ] Registro de usuario con email y contraseña (hash bcrypt).
- [ ] Login retorna JWT de acceso.
- [ ] Endpoints protegidos requieren JWT válido.
- [ ] El usuario solo accede a sus propios datos.
- [ ] Hay pruebas unitarias para auth y autorización.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- OAuth con Google/Apple (V2).
- MFA (V2).
- Roles y permisos avanzados (V2).