# Arquitectura del Agente: estilo Jarvis, personal para el cliente

> Agente único de la idea "Puente": el cliente solo habla con él. Todo lo demás (portales, gestores, pagos) ocurre detrás, invisible.

---

## 0. Visión: un Jarvis personal para tu vida administrativa migratoria

Como Jarvis para Iron Man, este agente:

- **Te conoce**: recuerda tu historia, tus documentos, tus preferencias, tus plazos.
- **Anticipa**: avisa antes de que venza algo, antes de que cambie una norma.
- **Actúa por vos**: con tu permiso, completa trámites sin que toques un portal.
- **Habla tu idioma**: voz, texto, lenguaje sencillo, sin jerga, en tu idioma y tono preferido.
- **Es tu único interlocutor**: no hay "ir al portal", "llamar al gestor", "pagar en el banco". Todo pasa por el agente.

El cliente tiene **un solo punto de contacto** para toda su vida administrativa migratoria.

---

## 1. Arquitectura de alto nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (único usuario)                  │
│   WhatsApp / Voz / App  →  "Necesito renovar mi permiso"       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CAPA DE INTERACCIÓN (Interface Layer)              │
│  - WhatsApp Business API  - Voz (STT/TTS)  - App móvil/web     │
│  - Normalización de mensajes  - Identificación del usuario      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              NÚCLEO DEL AGENTE (Agent Core)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Memoria     │  │  Personalidad│  │  Orquestador de      │  │
│  │  Personal    │  │  y Tono      │  │  Acciones            │  │
│  │ (perfil,     │  │ (voz, estilo,│  │ (planes, tareas,     │  │
│  │  docs,       │  │  idioma,     │  │  confirmaciones)     │  │
│  │  historial)  │  │  preferencias)│  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Motor de Razonamiento (LLM multimodal + RAG)            │   │
│  │  - Entiende la intención  - Planifica pasos              │   │
│  │  - Consulta normativa migratoria (RAG por país)          │   │
│  │  - Decide cuándo actuar vs. pedir confirmación           │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CAPA DE ACCIÓN (Action Layer) — invisible          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐  │
│  │ Portales   │  │ Gestores   │  │ Pagos      │  │ Citas    │  │
│  │ oficiales  │  │ verificados│  │ de tasas   │  │ y notif. │  │
│  │ (APIs/RPA) │  │ (marketplace)│  │ (tokenizado)│  │          │  │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CAPA DE DATOS Y SEGURIDAD (Data & Security)        │
│  - Expediente digital (W3C Verifiable Credentials)             │
│  - Cifrado E2E  - Soberanía de datos  - Auditoría de accesos  │
│  - Base de conocimiento (normativa por país)                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes del Núcleo del Agente

### 2.1 Memoria Personal (el "cerebro" del cliente)

El agente recuerda **todo** lo del cliente, organizado en:

| Bloque | Contenido | Ejemplo |
|---|---|---|
| **Perfil** | Nombre, nacionalidad, países de interés, idioma, tono preferido, preferencias de canal | "Prefiere audio, español rioplatense, WhatsApp" |
| **Expediente** | Documentos (pasaporte, título, apostillas, permisos) como credenciales verificables | "Pasaporte vence 2028-03-15; título apostillado válido en AR/ES" |
| **Historial** | Trámites realizados, resultados, gestores usados, pagos | "Renovación permiso 2025: aprobada en 12 días, gestor X" |
| **Contexto activo** | Trámite en curso, siguiente paso, pendientes | "Esperando cita en Migraciones; recordarle el 10/11" |
| **Preferencias** | Horarios de notificación, nivel de detalle, autonomía deseada | "Quiero que me confirmes antes de enviar cualquier cosa" |

La memoria es **persistente entre sesiones** y se actualiza con cada interacción. El cliente nunca repite información.

### 2.2 Personalidad y Tono (Jarvis-style)

El agente tiene una **personalidad configurable** por el cliente:

- **Nombre**: el cliente puede llamarlo como quiera ("Jarvis", "Asistente", "Mi gestor").
- **Tono**: formal, cercano, directo, empático. Adaptable al estado emocional del cliente.
- **Idioma**: español (variantes regionales), portugués, inglés, etc.
- **Nivel de detalle**: resumen ejecutivo vs. explicación paso a paso.
- **Proactividad**: cuánto anticipa y actúa sin preguntar (configurable por el cliente).

El agente **no es un chatbot genérico**: tiene voz propia, recuerda conversaciones pasadas y se adapta al cliente.

### 2.3 Orquestador de Acciones

El orquestador es el "director de orquesta" que:

1. **Recibe la intención** del cliente ("renovar permiso de residencia").
2. **Planifica** los pasos necesarios (qué documentos, qué portal, qué gestor, qué pago).
3. **Coordina** la Capa de Acción (portales, gestores, pagos, citas) de forma invisible.
4. **Pide confirmación** al cliente en los puntos críticos (antes de enviar, antes de pagar).
5. **Reporta** el estado y el resultado en lenguaje sencillo.

El orquestador mantiene un **plan vivo** del trámite en curso y puede re-planificar si algo cambia (ej. falta un documento, cambió una norma).

### 2.4 Motor de Razonamiento (LLM + RAG)

- **LLM multimodal**: entiende texto, voz y documentos (imágenes de pasaportes, PDFs).
- **RAG por país**: base de conocimiento con normativa migratoria actualizada de cada país. El agente consulta antes de responder o actuar.
- **Decisión de autonomía**: decide cuándo actuar solo (tareas rutinarias) vs. cuándo pedir confirmación (riesgo legal, pago, envío de documentos).
- **Detección de cambios normativos**: monitorea actualizaciones y avisa al cliente proactivamente.

---

## 3. Capa de Acción (invisible para el cliente)

El cliente nunca ve esta capa. El agente la coordina.

### 3.1 Portales oficiales (APIs / RPA certificado)

- Integración con APIs gubernamentales cuando existen (ej. portal de Migraciones).
- RPA certificado para portales sin API (con auditoría y trazabilidad).
- Cada acción queda registrada con evidencia (captura, número de trámite, fecha).

### 3.2 Marketplace de gestores verificados

- El agente selecciona el gestor adecuado según el trámite y el país.
- El gestor recibe el caso con todo el contexto (documentos, historial) — el cliente no habla con él directamente.
- El pago al gestor se libera por escrow al completar el trámite.
- La reputación del gestor se actualiza automáticamente.

### 3.3 Pagos de tasas

- Tarjeta del cliente tokenizada (el cliente la registra una vez con el agente).
- El agente paga tasas oficiales en nombre del cliente, con confirmación previa.
- Recibo y comprobante se guardan en el expediente.

### 3.4 Citas y notificaciones

- El agente agenda citas (presenciales o virtuales) y las agrega al calendario del cliente.
- Notifica con la anticipación configurada (ej. 60 días antes de vencimiento, 24 horas antes de una cita).
- Reagenda si es necesario, siempre con confirmación.

---

## 4. Capa de Datos y Seguridad

### 4.1 Expediente digital (W3C Verifiable Credentials)

- Cada documento es una credencial verificable: emitida por la autoridad correspondiente, verificable criptográficamente.
- El cliente controla qué comparte y con quién (self-sovereign identity).
- Un país puede verificar un documento de otro país sin pedir el original.

### 4.2 Privacidad por diseño

- **Cifrado end-to-end** de todos los documentos y conversaciones.
- **Soberanía de datos**: el cliente puede exportar o eliminar todo en cualquier momento.
- **Sin venta de datos** a terceros. Nunca.
- **Auditoría de accesos**: el cliente ve quién accedió a qué y cuándo.
- **Cumplimiento proactivo** con GDPR y leyes locales.

### 4.3 Base de conocimiento

- Normativa migratoria por país, actualizada y versionada.
- Plantillas de formularios, requisitos por trámite, tiempos estimados.
- Historial de cambios normativos para avisar a clientes afectados.

---

## 5. Flujo de ejemplo: "Renovar mi permiso de residencia"

```
Cliente (WhatsApp): "Hola, necesito renovar mi permiso de residencia."

Agente: "Hola, [nombre]. Tu permiso vence el 15 de marzo. Te ayudo a renovarlo.
         Para empezar, necesito confirmar algunos datos. ¿Seguís viviendo en
         la misma dirección que registramos?"

Cliente: "Sí."

Agente: "Perfecto. Ya tengo tu pasaporte, tu comprobante de domicilio y tu
         foto actualizada en tu expediente. El trámite requiere:
         1. Llenar el formulario oficial
         2. Pagar la tasa de $X
         3. Agendar cita en Migraciones
         ¿Autorizás que lo gestione por vos? Te confirmo antes de enviar
         cualquier cosa."

Cliente: "Sí, dale."

Agente: "Listo. Ya llené el formulario y pagué la tasa con tu tarjeta
         registrada. Tu cita quedó agendada para el 10 de noviembre a las 9:00
         en la oficina de Migraciones de [ciudad]. Te envío el comprobante
         y la ubicación. ¿Querés que te recuerde el día anterior?"

Cliente: "Sí, por favor."

Agente: "Hecho. Te aviso el 9 de noviembre. Cualquier novedad, te escribo.
         Tu expediente ya se actualizó con este trámite."
```

**El cliente solo habló con el agente.** Portales, pagos, citas y gestores (si hubo) quedaron invisibles.

---

## 6. Principios de diseño (Jarvis-style)

1. **Un solo interlocutor**: el agente es el único punto de contacto. Siempre.
2. **Memoria total**: el cliente nunca repite información.
3. **Proactividad configurable**: el agente anticipa y actúa según el nivel de autonomía que el cliente elija.
4. **Confirmación en puntos críticos**: antes de enviar, pagar o compartir documentos, siempre se pide confirmación explícita.
5. **Invisibilidad de la complejidad**: portales, gestores, RPA, pagos — todo ocurre detrás del agente.
6. **Transparencia de acciones**: el cliente puede ver en cualquier momento qué hizo el agente, cuándo y por qué.
7. **Personalidad propia**: el agente tiene nombre, tono y estilo elegidos por el cliente.
8. **Privacidad primero**: los datos son del cliente, cifrados y portables.

---

## 7. Stack tecnológico (resumen)

| Capa | Tecnología |
|---|---|
| Interacción | WhatsApp Business API, STT/TTS (voz), App móvil/web |
| Núcleo | LLM multimodal + RAG, motor de orquestación, memoria personal |
| Acción | APIs gubernamentales, RPA certificado, marketplace de gestores, pagos tokenizados |
| Datos | W3C Verifiable Credentials, DID (self-sovereign identity), cifrado E2E |
| Conocimiento | Base de normativa migratoria por país (versionada) |
| Infraestructura | Cloud con aislamiento por cliente, auditoría de accesos, compliance GDPR/local |

---

## 8. Boundaries

- **Always**: confirmación humana explícita antes de enviar documentos, pagar o compartir datos; cifrado E2E; auditoría de accesos.
- **Ask first**: cambiar nivel de autonomía del agente; sumar un nuevo país; usar un gestor nuevo.
- **Never**: dar asesoría jurídica vinculante; vender datos; actuar sin confirmación en puntos críticos; exponer la complejidad al cliente.

---

## Key Learnings:

1. El agente es el único interlocutor del cliente: portales, gestores y sistemas quedan invisibles detrás.
2. La arquitectura se organiza en 5 capas: Interacción → Núcleo (memoria, personalidad, orquestador, razonamiento) → Acción (invisible) → Datos/Seguridad.
3. La memoria personal es el "cerebro": el cliente nunca repite información; el agente recuerda documentos, historial, preferencias y contexto activo.
4. El orquestador planifica y coordina la Capa de Acción, pidiendo confirmación en puntos críticos.
5. La privacidad es por diseño: cifrado E2E, soberanía de datos, auditoría de accesos, sin venta de datos.
6. El flujo de ejemplo muestra cómo el cliente solo habla con el agente y recibe el resultado; todo lo demás es invisible.
