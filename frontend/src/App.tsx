import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useVoice } from "./hooks/useVoice";
import AdminPanel from "./AdminPanel";
import BeneficiaryActivation from "./BeneficiaryActivation";

type Msg = { role: "user" | "agent"; text: string; ts: number; sources?: string[] };
type Doc = { doc_type: string; status: string; expires: string | null };
type Notif = { text: string };

const seed: Msg[] = [
  { role: "agent", text: "Hola, soy Puente. Tu agente personal para trámites migratorios. ¿En qué te ayudo hoy?", ts: Date.now() },
];

export default function App() {
  const [msgs, setMsgs] = useState<Msg[]>(seed);
  const [input, setInput] = useState("");
  const [typing, setTyping] = useState(false);
  const [docs, setDocs] = useState<Doc[]>([]);
  const [notifs, setNotifs] = useState<Notif[]>([]);
  const [credential, setCredential] = useState<string>("");
  const [verifying, setVerifying] = useState(false);
  const [verifyResult, setVerifyResult] = useState<string>("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);
  const [activationOpen, setActivationOpen] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const handleVoiceResult = useCallback((text: string) => {
    send(text);
  }, []);

  const { listening, supported, start, stop, speak } = useVoice(handleVoiceResult);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, typing]);

  useEffect(() => {
    fetch("/api/expediente/")
      .then((r) => r.json())
      .then((data) => {
        setDocs(data.documents || []);
        setNotifs(data.notifications || []);
      })
      .catch(() => {});
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
      await new Promise((r) => setTimeout(r, 600));
      if (!res.ok) {
        const reply = "Hubo un problema al contactar al agente. Intentá de nuevo.";
        setMsgs((m) => [...m, { role: "agent", text: reply, ts: Date.now() }]);
        speak(reply);
        return;
      }
      const reply = data.answer || "Hubo un problema. Intentá de nuevo.";
      setMsgs((m) => [...m, { role: "agent", text: reply, ts: Date.now(), sources: data.sources || [] }]);
      speak(reply);
    } finally {
      setTyping(false);
    }
  }

  async function issueCredential() {
    const res = await fetch("/api/credentials/issue", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject_did: "did:example:user1", doc_type: "passport", issued_by: "AR" }),
    });
    const data = await res.json();
    setCredential(data.token || "");
  }

  async function verifyCredential() {
    if (!credential) return;
    setVerifying(true);
    const res = await fetch("/api/credentials/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: credential }),
    });
    const data = await res.json();
    setVerifyResult(data.valid ? "Válida ✓" : `Inválida: ${data.error}`);
    setVerifying(false);
  }

  function docColor(status: string) {
    if (status.startsWith("vence")) return "text-warn";
    if (status === "válido" || status === "apostillado") return "text-ok";
    return "text-slate-400";
  }

  return (
    <div className="h-full flex flex-col md:flex-row">
      {/* Mobile header */}
      <header className="md:hidden px-4 py-3 border-b border-line flex items-center justify-between bg-panel/80 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-accent2 flex items-center justify-center font-bold text-ink text-sm">P</div>
          <span className="font-semibold">Puente</span>
        </div>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} className="text-slate-300 text-xl">☰</button>
      </header>

      {/* Sidebar */}
      <aside className={`${sidebarOpen ? "flex" : "hidden"} md:flex w-full md:w-72 flex-col border-r border-line bg-panel/60 backdrop-blur absolute md:relative z-10 h-[calc(100%-56px)] md:h-full`}>
        <div className="px-6 py-5 border-b border-line hidden md:block">
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

        <div className="px-6 py-4 flex-1 overflow-y-auto">
          <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Expediente</div>
          <div className="space-y-2 text-sm">
            {docs.length === 0 && <div className="text-slate-500 text-xs">Cargando…</div>}
            {docs.map((d, i) => (
              <div key={i} className="flex justify-between">
                <span className="text-slate-400 capitalize">{d.doc_type}</span>
                <span className={`font-mono ${docColor(d.status)}`}>{d.status}</span>
              </div>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-line">
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Notificaciones</div>
            {notifs.length === 0 && <div className="text-slate-500 text-xs">Sin notificaciones</div>}
            {notifs.map((n, i) => (
              <div key={i} className="text-sm text-slate-300">{n.text}</div>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-line">
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-2">Credenciales verificables</div>
            <button
              onClick={issueCredential}
              className="w-full text-xs px-3 py-2 rounded-lg bg-accent/20 text-accent hover:bg-accent/30 transition mb-2"
            >
              Emitir credencial (pasaporte)
            </button>
            {credential && (
              <div className="space-y-2">
                <div className="text-xs text-slate-400 break-all font-mono bg-ink/50 p-2 rounded">{credential.slice(0, 60)}…</div>
                <button
                  onClick={verifyCredential}
                  disabled={verifying}
                  className="w-full text-xs px-3 py-2 rounded-lg bg-ok/20 text-ok hover:bg-ok/30 transition"
                >
                  {verifying ? "Verificando…" : "Verificar credencial"}
                </button>
                {verifyResult && <div className="text-xs text-slate-300">{verifyResult}</div>}
              </div>
            )}
          </div>
        </div>

        <div className="px-6 py-4 border-t border-line text-xs text-slate-500 font-mono">
          un solo interlocutor · todo invisible
        </div>
      </aside>

      {/* Main chat */}
      <main className="flex-1 flex flex-col min-w-0">
        <header className="px-6 py-4 border-b border-line flex items-center justify-between">
          <div>
            <div className="font-semibold">{adminOpen ? "Panel de administración" : "Conversación"}</div>
            <div className="text-xs text-slate-400">Agente Puente · WhatsApp / voz / app</div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setAdminOpen(!adminOpen)}
              className="px-3 py-2 rounded-lg text-sm bg-panel border border-line hover:bg-line/50 transition"
            >
              {adminOpen ? "Chat" : "Admin"}
            </button>
            <button
              onClick={() => setActivationOpen(!activationOpen)}
              className="px-3 py-2 rounded-lg text-sm bg-panel border border-line hover:bg-line/50 transition"
            >
              Cupo
            </button>
            {supported && !adminOpen && (
              <button
                onClick={listening ? stop : start}
                className={`px-4 py-2 rounded-lg font-medium transition ${listening ? "bg-warn text-ink animate-pulse" : "bg-accent text-ink hover:bg-accent/90"}`}
              >
                {listening ? "Escuchando…" : "Hablar"}
              </button>
            )}
          </div>
        </header>

        {adminOpen ? (
          <div className="flex-1 overflow-y-auto">
            <AdminPanel />
          </div>
        ) : activationOpen ? (
          <div className="flex-1 overflow-y-auto">
            <BeneficiaryActivation onActivated={() => setActivationOpen(false)} />
          </div>
        ) : (
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
                  {m.role === "agent" && m.sources && m.sources.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-line/50 text-xs text-slate-400">
                      <div className="font-mono mb-1">Fuentes:</div>
                      {m.sources.map((s, i) => (
                        <div key={i} className="text-slate-500">• {s}</div>
                      ))}
                    </div>
                  )}
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
        )}

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