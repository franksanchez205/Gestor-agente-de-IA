# AGENTS.md — Diseño del Agente Jarvis (Puente)

> Especificación completa del agente de IA estilo Jarvis para reutilizar en otro proyecto.
> El agente es el ÚNICO interlocutor del cliente; todo lo demás (portales, gestores, pagos, sistemas) queda invisible detrás.

---

## 1. Principio rector

**El agente IA es la ÚNICA interfaz del cliente.**

El cliente nunca interactúa con portales gubernamentales, gestores humanos, formularios ni sistemas de pago. Solo habla con el agente (WhatsApp, voz o app). El agente es el orquestador único: recibe la solicitud en lenguaje natural, coordina todo lo demás de forma invisible, y devuelve solo el resultado y el estado en lenguaje sencillo.

---

## 2. Arquitectura de alto nivel

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
│  │  - Consulta normativa (RAG por dominio/país)             │   │
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
│  - Base de conocimiento (normativa por dominio/país)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Componentes del Núcleo del Agente

### 3.1 Memoria Personal (el "cerebro" del cliente)

El agente recuerda **todo** lo del cliente, organizado en:

| Bloque | Contenido |
|---|---|
| **Perfil** | Nombre, nacionalidad, países/dominios de interés, idioma, tono preferido, preferencias de canal |
| **Expediente** | Documentos (pasaporte, título, permisos, etc.) como credenciales verificables |
| **Historial** | Trámites realizados, resultados, gestores usados, pagos |
| **Contexto activo** | Trámite en curso, siguiente paso, pendientes |
| **Preferencias** | Horarios de notificación, nivel de detalle, autonomía deseada |

La memoria es **persistente entre sesiones** y se actualiza con cada interacción. El cliente nunca repite información.

**Implementación (Python):**
```python
@dataclass
class PersonalMemory:
    profile: UserProfile
    documents: list[Document] = field(default_factory=list)
    history: list[CaseHistory] = field(default_factory=list)
    active_context: dict[str, Any] = field(default_factory=dict)
    preferences: dict[str, Any] = field(default_factory=dict)

    def to_prompt_context(self) -> str:
        # Serializa la memoria para inyectarla en el prompt del LLM
        ...
```

### 3.2 Personalidad y Tono (Jarvis-style)

El agente tiene una **personalidad configurable** por el cliente:

- **Nombre**: el cliente puede llamarlo como quiera ("Jarvis", "Asistente", "Mi gestor").
- **Tono**: formal, cercano, directo, empático. Adaptable al estado emocional del cliente.
- **Idioma**: español (variantes regionales), portugués, inglés, etc.
- **Nivel de detalle**: resumen ejecutivo vs. explicación paso a paso.
- **Proactividad**: cuánto anticipa y actúa sin preguntar (configurable por el cliente).

El agente **no es un chatbot genérico**: tiene voz propia, recuerda conversaciones pasadas y se adapta al cliente.

**Implementación (Python):**
```python
@dataclass
class Personality:
    agent_name: str = "Puente"
    tone: str = "cercano"
    language: str = "es"
    dialect: str = "rioplatense"
    detail_level: str = "resumen"
    proactivity: str = "media"

    def system_prompt(self) -> str:
        return (
            f"Sos {self.agent_name}, el agente personal de vida administrativa "
            f"migratoria del cliente. Hablás en {self.language} ({self.dialect}), "
            f"con tono {self.tone}. Nivel de detalle: {self.detail_level}. "
            f"Proactividad: {self.proactivity}. Nunca des asesoría jurídica "
            f"vinculante. Confirmá antes de enviar documentos, pagar o compartir datos."
        )
```

### 3.3 Orquestador de Acciones

El orquestador es el "director de orquesta" que:

1. **Recibe la intención** del cliente.
2. **Planifica** los pasos necesarios (qué documentos, qué portal, qué gestor, qué pago).
3. **Coordina** la Capa de Acción (portales, gestores, pagos, citas) de forma invisible.
4. **Pide confirmación** al cliente en los puntos críticos (antes de enviar, antes de pagar).
5. **Reporta** el estado y el resultado en lenguaje sencillo.

El orquestador mantiene un **plan vivo** del trámite en curso y puede re-planificar si algo cambia.

**Implementación (Python):**
```python
@dataclass
class PlanStep:
    step_id: str
    description: str
    action: Callable[[], Awaitable[dict]] | None = None
    requires_confirmation: bool = False
    status: StepStatus = StepStatus.PENDING
    result: dict | None = None

@dataclass
class TramitePlan:
    plan_id: str
    tramite: str
    country: str
    steps: list[PlanStep] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return len(self.steps) > 0 and all(s.status == StepStatus.DONE for s in self.steps)

class Orchestrator:
    def __init__(self, confirm_callback: Callable[[str], Awaitable[bool]]):
        self.confirm_callback = confirm_callback

    async def run(self, plan: TramitePlan) -> TramitePlan:
        for step in plan.steps:
            if step.status != StepStatus.PENDING:
                continue
            if step.requires_confirmation:
                step.status = StepStatus.AWAITING_CONFIRMATION
                ok = await self.confirm_callback(step.description)
                if not ok:
                    step.status = StepStatus.FAILED
                    break
            step.status = StepStatus.RUNNING
            try:
                if step.action is not None:
                    step.result = await step.action()
                step.status = StepStatus.DONE
            except Exception as exc:
                step.status = StepStatus.FAILED
                step.result = {"error": str(exc)}
                break
        return plan
```

### 3.4 Motor de Razonamiento (LLM + RAG)

- **LLM multimodal**: entiende texto, voz y documentos (imágenes de pasaportes, PDFs).
- **RAG por dominio/país**: base de conocimiento con normativa actualizada. El agente consulta antes de responder o actuar.
- **Decisión de autonomía**: decide cuándo actuar solo (tareas rutinarias) vs. cuándo pedir confirmación (riesgo legal, pago, envío de documentos).
- **Detección de cambios normativos**: monitorea actualizaciones y avisa al cliente proactivamente.

**Implementación (Python):**
```python
class ReasoningEngine:
    def __init__(self, llm_client, knowledge_base, system_prompt: str | None = None):
        self.llm = llm_client
        self.kb = knowledge_base
        self.system_prompt = system_prompt

    async def understand(self, user_message: str, memory_context: str, country: str | None = None) -> ReasoningResult:
        sources = await self.kb.search(user_message, country=country)
        prompt = self._build_prompt(user_message, memory_context, sources)
        raw = await self.llm.complete(prompt, system=self.system_prompt)
        return self._parse(raw, sources)
```

---

## 4. Capa de Acción (invisible para el cliente)

El cliente nunca ve esta capa. El agente la coordina.

### 4.1 Portales oficiales (APIs / RPA certificado)

- Integración con APIs gubernamentales cuando existen.
- RPA certificado para portales sin API (con auditoría y trazabilidad).
- Cada acción queda registrada con evidencia (captura, número de trámite, fecha).

### 4.2 Marketplace de gestores verificados

- El agente selecciona el gestor adecuado según el trámite y el país.
- El gestor recibe el caso con todo el contexto (documentos, historial) — el cliente no habla con él directamente.
- El pago al gestor se libera por escrow al completar el trámite.
- La reputación del gestor se actualiza automáticamente.

### 4.3 Pagos de tasas

- Tarjeta del cliente tokenizada (el cliente la registra una vez con el agente).
- El agente paga tasas oficiales en nombre del cliente, con confirmación previa.
- Recibo y comprobante se guardan en el expediente.

### 4.4 Citas y notificaciones

- El agente agenda citas (presenciales o virtuales) y las agrega al calendario del cliente.
- Notifica con la anticipación configurada (ej. 60 días antes de vencimiento, 24 horas antes de una cita).
- Reagenda si es necesario, siempre con confirmación.

---

## 5. Capa de Datos y Seguridad

### 5.1 Expediente digital (W3C Verifiable Credentials)

- Cada documento es una credencial verificable: emitida por la autoridad correspondiente, verificable criptográficamente.
- El cliente controla qué comparte y con quién (self-sovereign identity).
- Un país puede verificar un documento de otro país sin pedir el original.

### 5.2 Privacidad por diseño

- **Cifrado end-to-end** de todos los documentos y conversaciones.
- **Soberanía de datos**: el cliente puede exportar o eliminar todo en cualquier momento.
- **Sin venta de datos** a terceros. Nunca.
- **Auditoría de accesos**: el cliente ve quién accedió a qué y cuándo.
- **Cumplimiento proactivo** con GDPR y leyes locales.

### 5.3 Base de conocimiento

- Normativa por dominio/país, actualizada y versionada.
- Plantillas de formularios, requisitos por trámite, tiempos estimados.
- Historial de cambios normativos para avisar a clientes afectados.

---

## 6. LLM Client (unificado)

```python
class LLMClient:
    def __init__(self, provider: str = "openai", model: str | None = None, api_key: str | None = None):
        self.provider = provider.lower()
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            import openai
            self._client = openai.AsyncOpenAI(api_key=self.api_key)
            self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        elif self.provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            import anthropic
            self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
            self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        elif self.provider == "gemini":
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._genai = genai
            self.model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

    async def complete(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
        # Implementación por proveedor
        ...
```

---

## 7. Vector Store (RAG)

```python
class InMemoryVectorStore:
    def __init__(self):
        self._docs: list[dict] = []

    def add(self, text: str, metadata: dict | None = None) -> None:
        self._docs.append({"text": text, "metadata": metadata or {}})

    def search(self, query: str, top_k: int = 5, country: str | None = None) -> list[str]:
        # Búsqueda por similitud (en producción: embeddings + vector DB)
        ...

    def count(self) -> int:
        return len(self._docs)
```

En producción: usar pgvector (PostgreSQL) o ChromaDB con embeddings (OpenAI text-embedding-3-small).

---

## 8. Principios de diseño (Jarvis-style)

1. **Un solo interlocutor**: el agente es el único punto de contacto. Siempre.
2. **Memoria total**: el cliente nunca repite información.
3. **Proactividad configurable**: el agente anticipa y actúa según el nivel de autonomía que el cliente elija.
4. **Confirmación en puntos críticos**: antes de enviar, pagar o compartir documentos, siempre se pide confirmación explícita.
5. **Invisibilidad de la complejidad**: portales, gestores, RPA, pagos — todo ocurre detrás del agente.
6. **Transparencia de acciones**: el cliente puede ver en cualquier momento qué hizo el agente, cuándo y por qué.
7. **Personalidad propia**: el agente tiene nombre, tono y estilo elegidos por el cliente.
8. **Privacidad primero**: los datos son del cliente, cifrados y portables.

---

## 9. Boundaries

- **Always**: confirmación humana explícita antes de enviar documentos, pagar o compartir datos; cifrado E2E; auditoría de accesos; tests antes de commit.
- **Ask first**: cambiar de dominio/país; sumar un nuevo gestor; cambiar nivel de autonomía del agente.
- **Never**: dar asesoría jurídica vinculante; vender datos de usuarios; actuar sin confirmación en puntos críticos; recibir documentos sin cifrado E2E.

---

## 10. Stack tecnológico (resumen)

| Capa | Tecnología |
|---|---|
| Interacción | WhatsApp Business API, STT/TTS (voz), App web (React) |
| Núcleo | LLM (OpenAI/Anthropic/Gemini) + RAG, motor de orquestación, memoria personal |
| Acción | APIs gubernamentales, RPA certificado, marketplace de gestores, pagos tokenizados |
| Datos | W3C Verifiable Credentials, DID (self-sovereign identity), cifrado E2E |
| Conocimiento | Base de normativa por dominio/país (versionada) |
| Infraestructura | Cloud con aislamiento por cliente, auditoría de accesos, compliance GDPR/local |

---

## 11. Flujo de ejemplo

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

## 12. Notas de implementación

- El agente usa `load_dotenv()` para cargar variables de entorno.
- El LLM client selecciona el proveedor disponible (OpenAI → Anthropic → Gemini → mock).
- El RAG usa un vector store in-memory (extensible a pgvector/ChromaDB).
- La normativa se ingesta como `KnowledgeChunk` con país, trámite, fuente, contenido y fecha.
- El expediente digital usa W3C Verifiable Credentials (JWT-VC).
- El control de acceso usa tokens JWT de acceso temporal (share/revoke).
- La exportación/eliminación de datos garantiza la soberanía del cliente.

---

## Key Learnings

1. El agente es el único interlocutor del cliente: portales, gestores y sistemas quedan invisibles detrás.
2. La memoria personal es el "cerebro": el cliente nunca repite información.
3. El orquestador planifica y coordina la Capa de Acción, pidiendo confirmación en puntos críticos.
4. La privacidad es por diseño: cifrado E2E, soberanía de datos, auditoría de accesos, sin venta de datos.
5. El flujo de ejemplo muestra cómo el cliente solo habla con el agente y recibe el resultado; todo lo demás es invisible.
6. El diseño del panel (estilo Jarvis/Iron Man) usa: fondo oscuro con grid holográfico, orbes de glow, métricas animadas, ondas de voz, chat estilo terminal, tipografía monoespaciada para datos.