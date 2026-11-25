# 009 - Autenticación en frontend

## Objetivo

Agregar login y registro en el frontend, proteger rutas con JWT, y mostrar el usuario autenticado en la UI.

## Historias

- Como usuario, quiero registrarme desde el frontend.
- Como usuario, quiero iniciar sesión y obtener un token JWT.
- Como usuario, quiero que mis datos (expediente, trámites) estén protegidos.
- Como usuario, quiero cerrar sesión.

## Criterios de aceptación

- [ ] Formulario de registro en el frontend.
- [ ] Formulario de login en el frontend.
- [ ] Token JWT se guarda en localStorage.
- [ ] Rutas protegidas requieren token válido.
- [ ] El usuario ve su nombre/email en la UI.
- [ ] Logout limpia el token.
- [ ] Hay pruebas unitarias para auth en frontend.
- [ ] Cobertura de tests ≥ 80% en los módulos nuevos.

## Fuera de alcance

- OAuth con Google/Apple (V2).
- MFA (V2).