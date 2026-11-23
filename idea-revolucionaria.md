# Idea revolucionaria: Puente — el agente que actúa en tu nombre

> Evolución de la idea "Gestor" (PDF original), incorporando todas las recomendaciones de validación y llevándola a un concepto que todavía no existe en el mercado: un agente transfronterizo que no solo informa, sino que **ejecuta** trámites en tu nombre, con pago por éxito y credenciales verificables.

---

## 0. Por qué esto es revolucionario (y no otra app de trámites)

El mercado está saturado de **bots que responden** (gobiernos, empresas, copilotos genéricos). Lo que NO existe es un **agente que actúe por el ciudadano** a través de fronteras, con responsabilidad compartida y pago por resultado. Ese es el hueco real — y es enorme.

**Puente** no es una app de trámites. Es un **proxy administrativo personal**: un agente que, con tu consentimiento delegado, completa trámites en tu nombre, en varios países, y solo cobra si el trámite se completa exitosamente.

---

## 1. Propuesta de valor (en una frase)

> "Puente hace tus trámites migratorios por vos — en cualquier país — y solo cobra si salen bien."

## 1.1 Principio rector: el agente IA es la ÚNICA interfaz del cliente

El cliente **nunca** interactúa con portales gubernamentales, ni con gestores humanos, ni con formularios, ni con sistemas de pago. **Solo habla con el agente IA** (por WhatsApp, voz o app). El agente:

- Recibe la solicitud en lenguaje natural ("necesito renovar mi permiso de residencia").
- Coordina todo lo demás de forma invisible: documentos, portales oficiales, gestores humanos verificados, pagos de tasas, citas, notificaciones.
- Devuelve al cliente solo el resultado y el estado, en lenguaje sencillo.

Todo lo humano (gestores verificados) y todo lo institucional (portales, APIs, RPA) queda **detrás del agente**, invisible para el usuario. El agente es el orquestador único: el cliente tiene un solo interlocutor para toda su vida administrativa migratoria.

---

## 2. Diferenciadores revolucionarios (vs. idea original "Gestor")

| Dimensión | Gestor (original) | Puente (revolucionario) |
|---|---|---|
| Rol del agente | Informa y prepara | **Ejecuta en tu nombre** (acción delegada) |
| Cobro | Suscripción mensual | **Pago por éxito** (outcome-based) + suscripción opcional para monitoreo |
| Documentos | Expediente digital vivo | **Credenciales verificables transfronterizas** (W3C Verifiable Credentials) |
| Gestores humanos | Derivación simple | **Marketplace con reputación on-chain / transparente** |
| Privacidad | "Seguridad es core" | **Privacidad por diseño: cifrado E2E, datos del usuario son del usuario, portabilidad total** |
| Canal / Interfaz | WhatsApp + voz | **Solo el agente IA** (WhatsApp, voz, app). El agente es el único punto de contacto del cliente; portales, gestores y sistemas quedan detrás, invisibles. |
| Comunidad | No contemplada | **Red de migrantes con ayuda mutua + reputación** |
| Alcance inicial | 6+ trámites en 2 países | **1 país + 1 trámite** (validación real), escalando por vertical |

---

## 3. Las 5 innovaciones que marcan la diferencia

### 3.1 Agente que actúa (Action Agent), no solo conversa — y es el único interlocutor

El cliente **solo habla con el agente**. El agente no solo te dice "necesitás estos documentos"; con tu **consentimiento delegado explícito**, completa el trámite por vos y coordina todo lo demás de forma invisible:

- Llena formularios oficiales (vía APIs gubernamentales o RPA certificado).
- Sube documentos al portal correspondiente.
- Paga tasas en tu nombre (con tu tarjeta tokenizada).
- Agenda citas y te notifica.

**Cómo se evita el riesgo legal**: el agente actúa como "facilitador administrativo", no como asesor jurídico. Cada acción requiere confirmación humana explícita ("¿autorizás que Puente envíe tu pasaporte al portal de Migraciones?"). El gestor humano verificado revisa antes del envío final en casos de riesgo.

### 3.2 Credenciales verificables transfronterizas (W3C VC)

Tu expediente no es un PDF guardado. Es un **conjunto de credenciales verificables** (W3C Verifiable Credentials) que:

- Un país emite (ej. título universitario apostillado).
- Otro país verifica criptográficamente sin pedir el original.
- Vos controlás qué compartís y con quién (self-sovereign identity).

Esto elimina el "apostillar de nuevo" y el "validar tu título en cada país". Es la pieza que ningún bot institucional resuelve porque requiere interoperabilidad entre países.

### 3.3 Marketplace de gestores con reputación verificable

No es una lista de contactos. Es un marketplace donde:

- Los gestores se verifican (matrícula, antecedentes, referencias).
- Cada caso queda registrado con resultado (éxito/fallo/tiempo).
- La reputación es pública y no editable por el gestor.
- El pago al gestor se libera solo cuando el trámite se completa (escrow).

Esto resuelve el problema de "gestores informales" y crea un mercado de servicios migratorios de calidad.

### 3.4 Modelo de ingresos por éxito (outcome-based)

- **Pago por trámite completado** (ej. $X cuando se aprueba la renovación).
- **Suscripción opcional** para monitoreo proactivo (avisos de vencimiento, cambios normativos).
- **Plan familiar** (varios miembros, un solo pago).
- **B2B posterior**: ONG/organismos compran "cupos" para su población migrante.

Esto alinea los incentivos: Puente solo gana si vos ganás. Reduce el riesgo percibido y acelera la adopción.

### 3.5 Privacidad por diseño y soberanía de datos

- Cifrado end-to-end de documentos.
- Los datos son del usuario: exportables, eliminables, portables en cualquier momento.
- Sin venta de datos a terceros. Nunca.
- Auditoría de accesos: el usuario ve quién accedió a qué y cuándo.
- Cumplimiento proactivo con GDPR/leyes locales (no reactivo).

---

## 4. Segmento inicial y plan de expansión (scope disciplinado)

**MVP (V1)**: 1 país + 1 trámite de alto volumen y alto dolor.

Candidatos (elegir uno):
- Renovación de permiso de residencia (ej. Argentina, con alto flujo migratorio regional).
- Validación/apostilla de título universitario (alto dolor, multi-país).

**V2**: mismo país, 2-3 trámites adicionales + segundo país.
**V3**: multi-país + B2B (ONG/organismos) + marketplace de gestores maduro.
**V4**: credenciales verificables transfronterizas + APIs gubernamentales integradas.

---

## 5. Tecnología clave

- **LLM multimodal** (voz + texto + documentos) con RAG sobre normativa migratoria de cada país.
- **W3C Verifiable Credentials** para expediente interoperable.
- **Self-sovereign identity** (DID) para control del usuario.
- **RPA certificado + APIs oficiales** para ejecución de trámites.
- **Escrow + reputación** para marketplace de gestores.
- **Cifrado E2E** (zero-knowledge donde sea posible).

---

## 6. Modelo de negocio (resumen)

| Fuente | Descripción | Cuándo |
|---|---|---|
| Pago por trámite | Cobro al completar exitosamente | V1 |
| Suscripción proactiva | Monitoreo de vencimientos y cambios normativos | V1 |
| Plan familiar | Varios miembros, un pago | V1 |
| Marketplace de gestores | Comisión por derivación | V2 |
| B2B (ONG/organismos) | Cupos para población migrante | V3 |

---

## 7. Validación (incorporando todas las recomendaciones)

### 7.1 Claims a verificar (del análisis anterior)

| Claim | Acción de validación |
|---|---|
| 10% trámites online en Perú | Encuesta + datos INEI/RENIEC |
| 54% Salesforce | Verificar fuente exacta, contexto y segmento |
| 40% churn en 30 días | Benchmark de apps de servicios, no genérico |
| Volumen de búsqueda | Google Keyword Planner / Ahrefs (≥1 keyword ≥1.000/mes o cola larga viable) |
| Competencia | Mapear ≥10 jugadores (EE. UU. + LATAM) incluyendo Boundless, visabot, DoNotPay, bots institucionales |

### 7.2 Plan de validación (4-6 semanas)

1. **Elegir país + trámite MVP** (semana 1).
2. **Mapear competencia** (semana 1-2).
3. **Validar keywords y volúmenes** (semana 2).
4. **Entrevistas** con ≥15 migrantes del segmento (semana 2-4).
5. **Landing page con precio visible** → medir conversión a waitlist (≥5%) (semana 3-5).
6. **Validar WTP**: ≥30% dispuestos a pagar la suscripción propuesta (semana 4-6).
7. **Definir esquema legal/privacidad** antes de recibir documentos reales (paralelo, todo el período).

### 7.3 Success criteria (go/no-go)

- ≥ 1 trámite + 1 país definidos para MVP.
- Volúmenes de búsqueda validados.
- Competencia mapeada (≥10 jugadores).
- ≥15 entrevistas completadas.
- Landing: ≥5% conversión a waitlist con precio visible.
- WTP: ≥30% dispuestos a pagar.
- Esquema legal/privacidad documentado.

### 7.4 Boundaries

- **Always**: validar antes de construir; no recibir documentos reales sin esquema legal/privacidad; cada acción del agente requiere confirmación humana explícita.
- **Ask first**: elegir país/trámite MVP; cambiar de segmento; sumar un nuevo país.
- **Never**: dar asesoría jurídica vinculante; vender datos de usuarios; prometer automatización total sin gestor humano; recibir documentos sin cifrado E2E.

---

## 8. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Responsabilidad legal | Agente como facilitador, no asesor; confirmación humana explícita; gestores verificados |
| Privacidad | Cifrado E2E, datos del usuario son del usuario, auditoría de accesos |
| Competencia oculta | Mapeo profundo en fase de validación (≥10 jugadores) |
| Scope creep | 1 país + 1 trámite en MVP; Out of Scope explícito |
| Retención | Valor recurrente por vencimientos + cambios normativos |
| Confianza del usuario | Pago por éxito + reputación verificable de gestores + transparencia |

---

## 9. Roadmap

- **Semanas 1-6**: Validación (sin construir).
- **Meses 2-4**: MVP (1 país, 1 trámite, agente que actúa con confirmación humana).
- **Meses 5-8**: V2 (más trámites, segundo país, marketplace de gestores).
- **Meses 9-12**: V3 (multi-país, B2B, credenciales verificables).
- **Año 2**: V4 (APIs gubernamentales integradas, SSI completo).

---

## 10. Marketing (ideas aplicables, skill marketing-ideas)

- **Programmatic SEO**: cada trámite × país = página. Validar volúmenes primero.
- **Content & SEO**: guías de trámites migratorios (alta intención, cola larga).
- **Community + Reddit**: comunidades de migrantes donde está el usuario.
- **Founder-led sales**: entrevistas directas para validar WTP y canal.
- **Free tools**: calculadora de documentos por trámite/país → lead gen.
- **Waitlist referrals + early access pricing**: pre-launch.
- **Comment marketing**: autoridad en foros de migrantes.

---

## 11. Out of Scope (Deferred)

- Construcción del producto (hasta pasar validación).
- Multi-país/multi-trámite simultáneo (V2).
- B2B (ONG/organismos) (V3).
- Remesas, seguros, impuestos (V2+).
- Credenciales verificables transfronterizas (V3-V4).

---

## Key Learnings:

1. El hueco real no es "informar trámites" (saturado) sino "actuar por el ciudadano a través de fronteras" (no existe).
2. Las 5 innovaciones clave: (1) agente que actúa con confirmación humana, (2) credenciales verificables transfronterizas (W3C VC), (3) marketplace de gestores con reputación verificable, (4) pago por éxito (outcome-based), (5) privacidad por diseño.
3. El scope se disciplina a 1 país + 1 trámite en MVP; todo lo demás es Deferred.
4. El modelo de ingresos por éxito alinea incentivos y reduce riesgo percibido.
5. La validación debe medir WTP real (landing con precio, ≥5% conversión), no solo "probablemente usaría".
6. Skills aplicadas: `marketing-ideas` (growth) y `spec-driven-development` (spec de validación V1).
