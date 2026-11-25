import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

type Msg = { role: "user" | "agent"; text: string; ts: number; sources?: string[] };

const seed: Msg[] = [
  { role: "agent", text: "Buenos días. Todos los sistemas operativos. ¿En qué puedo ayudarte hoy?", ts: Date.now() },
];

export default function JarvisPanel({ onExit }: { onExit: () => void }) {
  const [msgs, setMsgs] = useState<Msg[]>(seed);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [pulse, setPulse] = useState(0);
  const bottomRef = useRef<HTMLDivElement>(null);



  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, typing]);

  useEffect(() => {
    const id = setInterval(() => setPulse((p) => (p + 1) % 100), 50);
    return () => clearInterval(id);
  }, []);

  async function send(text: string) {
    const t = text.trim();
    if (!t) return;
    setMsgs((m) => [...m, { role: "user", text: t, ts: Date.now() }]);
    setInput("");
    setTyping(true);
    try {
      const res = await fetch("/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: t }),
      });
      const data = await res.json();
      await new Promise((r) => setTimeout(r, 500));
      const reply = data.answer || "Procesando solicitud...";
      setMsgs((m) => [...m, { role: "agent", text: reply, ts: Date.now(), sources: data.sources || [] }]);
    } finally {
      setTyping(false);
    }
  }

  return (
    <div className="min-h-screen bg-[#050810] text-cyan-100 font-mono overflow-hidden relative">
      {/* Grid background */}
      <div className="absolute inset-0 opacity-20" style={{
        backgroundImage: "linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,255,0.03) 1px, transparent 1px)",
        backgroundSize: "40px 40px",
      }} />

      {/* Glow orbs */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />

      <div className="relative z-10 flex flex-col h-screen">
        {/* Header */}
        <header className="px-6 py-4 border-b border-cyan-500/20 flex items-center justify-between backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-10 h-10 border-2 border-cyan-400 rounded-full flex items-center justify-center"
            >
              <div className="w-6 h-6 border border-cyan-300 rounded-full" />
            </motion.div>
            <div>
              <h1 className="text-xl font-bold tracking-widest text-cyan-300">PUENTE</h1>
              <p className="text-xs text-cyan-500/70 tracking-wider">SISTEMA OPERATIVO · v2.0</p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-xs">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              <span className="text-emerald-400">ONLINE</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" />
              <span className="text-cyan-400">LLM: CONECTADO</span>
            </div>
            <div className="text-cyan-500/70">
              {new Date().toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" })}
            </div>
            <button
              onClick={onExit}
              className="px-3 py-1 rounded border border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10 transition-colors text-xs"
            >
              SALIR
            </button>
          </div>
        </header>

        {/* Main grid */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4 p-4 overflow-hidden">
          {/* Left: Status panels */}
          <div className="hidden lg:flex flex-col gap-4">
            {/* System status */}
            <div className="bg-cyan-950/30 border border-cyan-500/20 rounded-xl p-4 backdrop-blur">
              <h3 className="text-xs uppercase tracking-widest text-cyan-400 mb-3">Estado del sistema</h3>
              <div className="space-y-2 text-xs">
                {[
                  { label: "CPU", value: 34 + (pulse % 10), color: "bg-cyan-400" },
                  { label: "MEM", value: 62, color: "bg-blue-400" },
                  { label: "RED", value: 78, color: "bg-emerald-400" },
                  { label: "DISCO", value: 45, color: "bg-amber-400" },
                ].map((m) => (
                  <div key={m.label} className="flex items-center gap-2">
                    <span className="w-12 text-cyan-500/70">{m.label}</span>
                    <div className="flex-1 h-1.5 bg-cyan-900/50 rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full ${m.color} rounded-full`}
                        animate={{ width: `${m.value}%` }}
                        transition={{ duration: 0.5 }}
                      />
                    </div>
                    <span className="w-8 text-right text-cyan-300">{m.value}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Expediente */}
            <div className="bg-cyan-950/30 border border-cyan-500/20 rounded-xl p-4 backdrop-blur">
              <h3 className="text-xs uppercase tracking-widest text-cyan-400 mb-3">Expediente digital</h3>
              <div className="space-y-2 text-xs">
                {[
                  { icon: "🛂", label: "Pasaporte", status: "VÁLIDO", color: "text-emerald-400" },
                  { icon: "📋", label: "Permiso residencia", status: "VENCE 30D", color: "text-amber-400" },
                  { icon: "🎓", label: "Título", status: "APOSTILLADO", color: "text-emerald-400" },
                ].map((d) => (
                  <div key={d.label} className="flex items-center justify-between py-1">
                    <span className="flex items-center gap-2">
                      <span>{d.icon}</span>
                      <span className="text-cyan-200">{d.label}</span>
                    </span>
                    <span className={`font-mono ${d.color}`}>{d.status}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Notificaciones */}
            <div className="bg-cyan-950/30 border border-cyan-500/20 rounded-xl p-4 backdrop-blur">
              <h3 className="text-xs uppercase tracking-widest text-cyan-400 mb-3">Alertas</h3>
              <div className="text-xs text-amber-300 bg-amber-500/10 border border-amber-500/20 rounded-lg p-2">
                ⚠ Permiso de residencia vence en 30 días. ¿Gestiono la renovación?
              </div>
            </div>
          </div>

          {/* Center: Chat + Voice visualization */}
          <div className="lg:col-span-2 flex flex-col gap-4">
            {/* Voice waveform */}
            <div className="bg-cyan-950/30 border border-cyan-500/20 rounded-xl p-4 backdrop-blur flex items-center justify-center h-24">
              <div className="flex items-end gap-1 h-16">
                {Array.from({ length: 32 }).map((_, i) => (
                  <motion.div
                    key={i}
                    className="w-1 bg-cyan-400 rounded-full"
                    animate={{
                      height: [4, Math.random() * 40 + 8, 4],
                    }}
                    transition={{
                      duration: 0.8 + Math.random() * 0.4,
                      repeat: Infinity,
                      delay: i * 0.05,
                    }}
                  />
                ))}
              </div>
            </div>

            {/* Chat */}
            <div className="flex-1 bg-cyan-950/20 border border-cyan-500/20 rounded-xl backdrop-blur flex flex-col overflow-hidden">
              <div className="px-4 py-2 border-b border-cyan-500/20 text-xs text-cyan-400 tracking-wider">
                CANAL DE COMUNICACIÓN
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                <AnimatePresence initial={false}>
                  {msgs.map((m) => (
                    <motion.div
                      key={m.ts}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-[70%] rounded-lg px-4 py-2 text-sm ${
                          m.role === "user"
                            ? "bg-cyan-500/20 border border-cyan-400/30 text-cyan-100"
                            : "bg-blue-950/40 border border-cyan-500/20 text-cyan-200"
                        }`}
                      >
                        <div className="text-[10px] text-cyan-500/60 mb-1 tracking-wider">
                          {m.role === "user" ? "USUARIO" : "PUENTE"}
                        </div>
                        {m.text}
                        {m.role === "agent" && m.sources && m.sources.length > 0 && (
                          <div className="mt-2 pt-1 border-t border-cyan-500/10 text-[10px] text-cyan-500/60">
                            <div className="text-cyan-400/80 mb-1 tracking-wider">FUENTES RAG:</div>
                            {m.sources.map((s, i) => (
                              <div key={i} className="text-cyan-500/60">▸ {s}</div>
                            ))}
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {typing && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                    <div className="bg-blue-950/40 border border-cyan-500/20 rounded-lg px-4 py-2">
                      <div className="flex gap-1 items-center">
                        <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" />
                        <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: "200ms" }} />
                        <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: "400ms" }} />
                      </div>
                    </div>
                  </motion.div>
                )}
                <div ref={bottomRef} />
              </div>

              {/* Input */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  send(input);
                }}
                className="px-4 py-3 border-t border-cyan-500/20 flex gap-2"
              >
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Comando o consulta…"
                  className="flex-1 bg-cyan-950/30 border border-cyan-500/30 rounded-lg px-4 py-2 text-sm text-cyan-100 placeholder-cyan-500/40 focus:outline-none focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400/30 transition-colors font-mono"
                />
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-cyan-500/20 border border-cyan-400/30 text-cyan-300 font-medium hover:bg-cyan-500/30 transition-colors"
                >
                  ENVIAR
                </button>
              </form>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="px-6 py-2 border-t border-cyan-500/20 flex items-center justify-between text-[10px] text-cyan-500/50 tracking-wider">
          <span>PUENTE OS v2.0 · SISTEMA OPERATIVO MIGRATORIO</span>
          <span>UN SOLO INTERLOCUTOR · TODO INVISIBLE</span>
        </footer>
      </div>
    </div>
  );
}