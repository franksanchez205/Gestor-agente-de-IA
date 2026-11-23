# AGENTS.md

Puente: agente de IA para la vida administrativa migratoria.

## Documentación

- Producto: docs/product.md
- Stack: docs/tech-stack.md
- Arquitectura: docs/architecture.md
- Specs: docs/specs/NNN-nombre/

## Flujo de trabajo

1. No escribas código sin una spec aprobada.
2. Antes de programar, escribe plan.md (con su sección de Pruebas) y tasks.md en la carpeta de la spec.
3. Haz una task a la vez, con sus pruebas, y márcala con [x] solo si las pruebas pasan.
4. Si algo cambia a mitad de camino, corrige primero la spec, después el código.

## Comandos

- Infra: docker compose up -d db redis
- Pruebas DB: docker exec gestoragentedeiaparalavida-db-1 psql -U puente -d puente -c "SELECT 1;"
- Pruebas Redis: docker exec gestoragentedeiaparalavida-redis-1 redis-cli ping
- Backend: uvicorn src.main:app --reload (puerto 8000)
- Pruebas: pytest
- Lint: ruff check . && ruff format .

## Reglas

- Toda spec debe tener pruebas unitarias.
- No agregues dependencias sin preguntar.
- Código y nombres en inglés, docs en español.
- El agente es el único interlocutor del cliente; portales, gestores y sistemas quedan invisibles detrás.
- Nunca dar asesoría jurídica vinculante; confirmar antes de enviar documentos, pagar o compartir datos.
- Cifrado E2E y soberanía de datos desde el día 1.