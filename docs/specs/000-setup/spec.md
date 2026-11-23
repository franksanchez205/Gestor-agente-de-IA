# 000 - Setup del proyecto

## Objetivo

Tener el backend (FastAPI) y la infraestructura (PostgreSQL + Redis) arrancando y comunicándose, con al menos una prueba unitaria que pase.

## Historias

- Como desarrollador, quiero levantar la infraestructura con un comando.
- Como desarrollador, quiero ejecutar las pruebas con un comando.
- Como desarrollador, quiero un health check que confirme que la app está viva.

## Criterios de aceptación

- [ ] `docker compose up -d db redis` levanta PostgreSQL y Redis sin errores.
- [ ] `psql SELECT 1` responde OK.
- [ ] `redis-cli PING` responde PONG.
- [ ] `uvicorn src.main:app --reload` arranca en puerto 8000.
- [ ] `GET http://localhost:8000/health` responde `{"status": "ok"}`.
- [ ] `pytest` pasa con al menos una prueba unitaria.

## Fuera de alcance

- Funcionalidad de trámites (spec 001).
- Base de datos con modelos (spec 001).
- Canales WhatsApp/voz completos (spec 001).