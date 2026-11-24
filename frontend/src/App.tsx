import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

type Msg = { role: "user" | "agent"; text: string; ts: number };

const seed: Msg[] = [
  { role: "agent", text: "Hola, soy Puente. Tu agente personal para trámites migratorios. ¿En qué te ayudo hoy?", ts: Date.now() },
];

export default function App() {
  const [msgs, setMsgs] = useState<Msg[]>(seed);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [listening, setListening] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, typing]);

  async function send(text: string) {
    const t = text.trim();
    if (!t) return;
    setMsgs((m) => [...m, { role: "user", text: t, ts: Date.now() }]);
    setInput("");
    setTyping(true);
    try {
      const res = await fetch("/whatsapp/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: t }),
      });
      const data = await res.json();
      await new Promise((r) => setTimeout(r, 600));
      setMsgs((m) => [
        ...m,
        {
          role: "agent",
          text:
            data.status === "ok"
              ? "Recibí tu solicitud. Estoy preparando el plan del trámite; te confirmo antes de enviar cualquier cosa. ¿Autorizás que gestione por vos?"
              : "Hubo un problema. Intentá de nuevo.",
          ts: Date.now(),
        },
      ]);
    } finally {
      setTyping(false);
    }
  }

  function toggleVoice() {
    setListening((v) => !v);
    if (!listening) {
      // Placeholder: integración con Web Speech API
      setTimeout(() => {
        setListening(false);
        send("Necesito renovar mi permiso de residencia");
      }, 1200);
    }
  }

  return (
    <div className="h-full flex">
      {/* Sidebar */}
      <aside className="hidden md:flex w-72 flex-col border-r border-line bg-panel/60 backdrop-blur">
        <div className="px-6 py-5 border-b border-line">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-accent to-accent2 flex items-center justify-center font-bold text-ink">
              P
            </div>
            <div>
              <div className="font-semibold tracking-tight">Puente</div>
              <div className="text-xs text-slate-400 font-mono">agente personal</div>
            </div>
          </div>
        </div>

        <div className="px-6 py-4">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Expediente</div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between"><span className="text-slate-400">Pasaporte</span><span className="font-mono text-ok">válido</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Permiso residencia</span><span className="font-mono text-warn">vence 30d</span></div>
            <div className="flex justify-between"><span className="text-slate-400">Título</span><span className="font-mono text-ok">apostillado</span></div>
          </div>
        </div>

        <div className="px-6 py-4 border-t border-line">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Notificaciones</div>
          <div className="text-sm text-slate-300">Tu permiso de residencia vence en 30 días. ¿Gestiono la renovación?</div>
        </div>

        <div className="mt-auto px-6 py-4 border-t border-line text-xs text-slate-500 font-mono">
          un solo interlocutor · todo invisible
        </div>
      </aside>

      {/* Main chat */}
      <main className="flex-1 flex flex-col">
        <header className="px-6 py-4 border-b border-line flex items-center justify-between">
          <div>
            <div className="font-semibold">Conversación</div>
            <div className="text-xs text-slate-400">Agente Puente · WhatsApp / voz / app</div>
          </div>
          <button
            onClick={toggleVoice}
            className={`px-4 py-2 rounded-lg font-medium transition ${listening ? "bg-warn text-ink" : "bg-accent text-ink hover:bg-accent/90"}`}
          >
            {listening ? "Escuchando…" : "Hablar"}
          </button>
        </header>

        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4">
          <AnimatePresence initial={false}>
            {msgs.map((m) => (
              <motion.div
                key={m.ts}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25 }}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    m.role === "user"
                      ? "bg-accent text-ink rounded-br-sm"
                      : "bg-panel border border-line text-slate-200 rounded-bl-sm"
                  }`}
                >
                  {m.text}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {typing && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="bg-panel border border-line rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </motion.div>
          )}
          <div ref={bottomRef} />
        </div>

        <form
          onSubmit={(e) => {
            e.preventDefault();
            send(input);
          }}
          className="px-6 py-4 border-t border-line flex gap-3"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribí tu mensaje…"
            className="flex-1 bg-panel border border-line rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            className="px-5 py-3 rounded-xl bg-accent text-ink font-medium hover:bg-accent/90 transition"
          >
            Enviar
          </button>
        </form>
      </main>
    </div>
  );
}