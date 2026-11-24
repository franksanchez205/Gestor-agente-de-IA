# Plan 003

## Stack

- React 18 + Vite + TypeScript
- Tailwind CSS (paleta custom: ink, panel, line, accent, accent2, ok, warn)
- Framer Motion (animaciones sutiles)
- Fuentes: Space Grotesk (sans) + JetBrains Mono (mono)

## Diseño

- Layout: sidebar (expediente + notificaciones) + chat principal.
- Paleta: oscuro profundo (radial gradient), acento azul eléctrico + violeta.
- Tipografía: Space Grotesk (no Inter/Roboto), JetBrains Mono para datos.
- Animaciones: fade-in de mensajes, typing indicator, una sola secuencia orquestada.

## Componentes

- App (layout principal)
- Sidebar (expediente, notificaciones)
- Chat (mensajes, input, typing)
- VoiceButton (toggle voz)

## Pruebas

- Build de producción pasa.
- Responsive verificado manualmente.
- Accesibilidad: focus visible, reduced motion.