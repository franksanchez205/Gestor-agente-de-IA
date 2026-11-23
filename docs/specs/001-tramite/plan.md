# Plan 001

## Datos

- Modelos: User, Document, Case (SQLAlchemy).
- Credenciales verificables (W3C VC) en el expediente.
- Memoria personal (perfil, documentos, historial, contexto, preferencias).

## Agente

- Orquestador de acciones (plan de trámite, confirmaciones).
- Motor de razonamiento (LLM + RAG normativa migratoria).
- Personalidad configurable (nombre, tono, idioma, proactividad).
- Notificaciones proactivas (vencimientos, cambios normativos).

## Capa de acción (invisible)

- Portales oficiales (APIs/RPA).
- Pagos de tasas (tokenizados, con confirmación).
- Citas y recordatorios.
- Marketplace de gestores verificados (futuro).

## Canales

- WhatsApp (webhook).
- Voz (STT/TTS).

## Pruebas

- Unit: memoria, orquestador, razonamiento, notificaciones.
- Integration: portales (sandbox), pagos (sandbox).
- E2E: flujo completo (WhatsApp → agente → resultado).