---
type: reference
audience: developer
---

# Referencia de módulos

## src/agent/memory.py

Memoria personal del agente (Jarvis-style).

- `UserProfile`: perfil del cliente (nombre, nacionalidad, países, idioma, tono, canal, horarios de notificación).
- `Document`: documento del expediente (tipo, emisor, fechas, credencial verificable).
- `CaseHistory`: historial de trámites (id, trámite, país, fechas, resultado, gestor).
- `PersonalMemory`: memoria persistente con métodos `add_document`, `expiring_soon`, `to_prompt_context`.

## src/agent/orchestrator.py

Orquestador de acciones del agente.

- `PlanStep`: paso del plan (id, descripción, acción, requiere confirmación, estado, resultado).
- `TramitePlan`: plan de trámite (id, trámite, país, pasos, `next_pending`, `is_complete`).
- `Orchestrator`: coordina la ejecución, pide confirmación en puntos críticos, marca done/failed.

## src/agent/reasoning.py

Motor de razonamiento (LLM + RAG).

- `ReasoningEngine.understand(message, memory_context)`: consulta la KB (RAG), construye prompt con memoria + fuentes, llama al LLM, retorna `ReasoningResult`.
- `ReasoningResult`: intent, country, tramite, answer, sources, needs_confirmation.

## src/agent/notifications.py

Notificaciones proactivas.

- `NotificationService.check_expiring_documents(memory, days_ahead)`: avisa documentos por vencer.
- `NotificationService.remind_appointment(appointment, hours_before)`: recordatorio de cita.

## src/agent/personality.py

Personalidad configurable del agente.

- `Personality`: nombre, tono, idioma, dialecto, nivel de detalle, proactividad. Método `system_prompt()`.

## src/action/portals.py

Integración con portales oficiales (APIs/RPA).

- `PortalClient`: `submit_form(form_data, documents)` → `PortalResult`; `check_status(tramite_number)` → str.
- `PortalResult`: success, tramite_number, message, evidence.

## src/action/payments.py

Pagos de tasas oficiales (tokenizados).

- `PaymentClient`: `pay_fee(amount, currency, tramite_number)` → `PaymentResult`.

## src/action/appointments.py

Agenda de citas y recordatorios.

- `AppointmentService`: `schedule()`, `reschedule()`.

## src/action/gestores.py

Marketplace de gestores verificados.

- `GestorMarketplace`: `find_best()`, `assign()`, `release_payment()`.

## src/data/models.py

Modelos SQLAlchemy: `User`, `Document`, `Case`, `Gestor`, `Payment`, `Credential` (V2/V4). `Case` incluye `title` (V2) para identificar el trámite. `Gestor` incluye specialties, verified, reputation_score, cases_completed. `Payment` incluye amount, currency, status (pending/released/refunded), escrow para gestores. `Credential` almacena JWT-VC (vc_jwt, issued_at, expires_at, revoked).

## src/api/whatsapp.py / voice.py

Canales de interacción: webhook de WhatsApp, STT/TTS de voz.

## src/knowledge/base.py

Base de conocimiento (RAG) por país.

- `KnowledgeBase`: `search(query, country, top_k)`, `ingest(chunks)`, `countries`, `has_country`.

## src/credentials/vc.py

Credenciales verificables (W3C Verifiable Credentials, JWT-VC).

- `issue_vc`, `verify_vc`, `is_vc_valid`, `VCError`.

## src/credentials/verifier.py

Verificador de credenciales con validaciones adicionales.

- `CredentialVerifier`: `verify(token, expected_subject)`, `is_valid(token, expected_subject)`. Valida issuer y subject esperados.

## src/credentials/access.py

Control de acceso a credenciales verificables.

## src/credentials/data_export.py

Exportación y eliminación de datos del usuario (soberanía de datos).

- `DataExporter`: `export_user_data(user_id)` → dict con profile, documents, cases, credentials. `delete_user_data(user_id)` → bool.

- `CredentialAccess`: `share(credential_id, expires_in_minutes)` → token JWT de acceso temporal. `revoke_share(share_token)` → bool. `check_access(share_token)` → bool. `revoke_credential(credential_id, revoked_set)`.

- `issue_vc(subject_did, claims, issuer_did, secret_key, expires_in_days, algorithm)` → JWT string.
- `verify_vc(token, secret_key, algorithms)` → payload dict o raise VCError.
- `is_vc_valid(token, secret_key)` → bool.
- `VCError`: excepción para credenciales inválidas/expiradas.

## frontend/

App web React + Vite + Tailwind (puerto 5173).

- `src/App.tsx`: layout principal (sidebar + chat). Diseño distintivo: paleta ink/panel/accent, tipografía Space Grotesk + JetBrains Mono, animaciones framer-motion.
- `src/main.tsx`: entry point.
- `src/index.css`: estilos base + radial gradient.
- Componentes: chat (mensajes, input, typing), sidebar (expediente, notificaciones), botón de voz.