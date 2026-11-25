import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useVoice } from "./hooks/useVoice";
import { getToken, clearToken, getUser, isAuthenticated } from "./auth";
import AdminPanel from "./AdminPanel";
import BeneficiaryActivation from "./BeneficiaryActivation";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

type Msg = { role: "user" | "agent"; text: string; ts: number; sources?: string[] };
type Doc = { doc_type: string; status: string; expires: string | null };
type Notif = { text: string };

const seed: Msg[] = [
  { role: "agent", text: "Hola, soy Puente. Tu agente personal para trámites migratorios. ¿En qué te ayudo hoy?", ts: Date.now() },
];

const docIcons: Record<string, string> = {
  passport: "🛂",
  permit: "📋",
  title: "🎓",
  apostille: "📜",
};

const docLabels: Record<string, string> = {
  passport: "Pasaporte",
  permit: "Permiso de residencia",
  title: "Título universitario",
  apostille: "Apostilla",
};

export default function App() {
  const [authenticated, setAuthenticated] = useState(isAuthenticated());
  const [showRegister, setShowRegister] = useState(false);
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
  const user = getUser();

  const handleVoiceResult = useCallback((text: string) => {
    send(text);
  }, []);

  const { listening, supported, start, stop, speak } = useVoice(handleVoiceResult);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, typing]);

  useEffect(() => {
    if (!authenticated) return;
    fetch("/api/expediente/", {
      headers: { Authorization: `Bearer ${getToken()}` },
    })
      .then((r) => r.json())
      .then((data) => {
        setDocs(data.documents || []);
        setNotifs(data.notifications || []);
      })
      .catch(() => {});
  }, [authenticated]);

  async function send(text: string) {
    const t = text.trim();
    if (!t) return;
    setMsgs((m) => [...m, { role: "user", text: t, ts: Date.now() }]);
    setInput("");
    setTyping(true);
    try {
      const res = await fetch("/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${getToken()}`,
        },
        body: JSON.stringify({ message: t }),
      });
      const data = await res.json();
      await new Promise((r) => setTimeout(r, 400));
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
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`,
      },
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

  function handleLogout() {
    clearToken();
    setAuthenticated(false);
    setMsgs(seed);
  }

  function docColor(status: string) {
    if (status.startsWith("vence")) return "text-amber-400";
    if (status === "válido" || status === "apostillado") return "text-emerald-400";
    return "text-slate-400";
  }

  // Auth gate
  if (!authenticated) {
    return showRegister ? (
      <RegisterForm onRegister={() => setAuthenticated(true)} />
    ) : (
      <div>
        <LoginForm onLogin={() => setAuthenticated(true)} />
        <div className="text-center mt-4">
          <button onClick={() => setShowRegister(true)} className="text-sm text-accent hover:underline">
            ¿No tenés cuenta? Registrate
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col md:flex-row">
      {/* Mobile header */}
      <header className="md:hidden px-4 py-3 border-b border-line flex items-center justify-between bg-panel/80 backdrop-blur">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-accent2 flex items-center justify-center font-bold text-ink text-sm">P</div>
          <span className="font-semibold">Puente</span>
        </div>
        <button onClick={() => setSidebarOpen(!sidebarOpen)} aria-label="Abrir menú" className="text-slate-300 text-xl focus-visible:ring-2 focus-visible:ring-accent">☰</button>
      </header>

      {/* Sidebar */}
      <aside className={`${sidebarOpen ? "flex" : "hidden"} md:flex w-full md:w-80 flex-col border-r border-line bg-panel/60 backdrop-blur absolute md:relative z-10 h-[calc(100%-56px)] md:h-full`}>
        <div className="px-6 py-5 border-b border-line hidden md:block">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent to-accent2 flex items-center justify-center font-bold text-ink text-lg shadow-lg shadow-accent/20">
              P
            </div>
            <div>
              <div className="font-semibold tracking-tight text-lg">Puente</div>
              <div className="text-xs text-slate-400 font-mono">tu agente personal</div>
            </div>
          </div>
        </div>

        <div className="px-6 py-4 flex-1 overflow-y-auto space-y-5">
          {/* Expediente */}
          <section>
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
              <span>Expediente digital</span>
              <span className="flex-1 h-px bg-line" />
            </div>
            <div className="space-y-2">
              {docs.length === 0 && <div className="text-slate-500 text-xs animate-pulse">Cargando…</div>}
              {docs.map((d, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-center justify-between py-1.5"
                >
                  <span className="flex items-center gap-2 text-sm text-slate-300">
                    <span aria-hidden="true">{docIcons[d.doc_type] || "📄"}</span>
                    <span>{docLabels[d.doc_type] || d.doc_type}</span>
                  </span>
                  <span className={`text-xs font-mono ${docColor(d.status)}`}>{d.status}</span>
                </motion.div>
              ))}
            </div>
          </section>

          {/* Notificaciones */}
          <section>
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
              <span>Notificaciones</span>
              <span className="flex-1 h-px bg-line" />
            </div>
            {notifs.length === 0 && <div className="text-slate-500 text-xs">Sin notificaciones</div>}
            {notifs.map((n, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                className="text-sm text-slate-300 bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2"
              >
                {n.text}
              </motion.div>
            ))}
          </section>

          {/* Credenciales */}
          <section>
            <div className="text-xs uppercase tracking-wider text-slate-500 mb-3 flex items-center gap-2">
              <span>Credenciales verificables</span>
              <span className="flex-1 h-px bg-line" />
            </div>
            <button
              onClick={issueCredential}
              className="w-full text-xs px-3 py-2 rounded-lg bg-accent/15 text-accent hover:bg-accent/25 transition-colors mb-2 border border-accent/20"
            >
              Emitir credencial (pasaporte)
            </button>
            {credential && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-2">
                <div className="text-xs text-slate-400 break-all font-mono bg-ink/50 p-2 rounded border border-line">
                  {credential.slice(0, 80)}…
                </div>
                <button
                  onClick={verifyCredential}
                  disabled={verifying}
                  className="w-full text-xs px-3 py-2 rounded-lg bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25 transition-colors border border-emerald-500/20 disabled:opacity-50"
                >
                  {verifying ? "Verificando…" : "Verificar credencial"}
                </button>
                {verifyResult && <div className="text-xs text-slate-300 text-center">{verifyResult}</div>}
              </motion.div>
            )}
          </section>
        </div>

        <div className="px-6 py-4 border-t border-line">
          <div className="text-xs text-slate-400 mb-2 truncate">{user?.user_id || "Usuario"}</div>
          <button onClick={handleLogout} className="text-xs text-red-400 hover:underline">
            Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Main chat */}
      <main className="flex-1 flex flex-col min-w-0">
        <header className="px-6 py-4 border-b border-line flex items-center justify-between">
          <div>
            <div className="font-semibold">Conversación</div>
            <div className="text-xs text-slate-400">Agente Puente · WhatsApp / voz / app</div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setAdminOpen(!adminOpen)}
              className="px-3 py-2 rounded-lg text-sm bg-panel border border-line hover:bg-line/50 transition-colors"
            >
              {adminOpen ? "Chat" : "Admin"}
            </button>
            <button
              onClick={() => setActivationOpen(!activationOpen)}
              className="px-3 py-2 rounded-lg text-sm bg-panel border border-line hover:bg-line/50 transition-colors"
            >
              Cupo
            </button>
            {supported && !adminOpen && !activationOpen && (
              <button
                onClick={listening ? stop : start}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${listening ? "bg-amber-500 text-ink animate-pulse" : "bg-accent text-ink hover:bg-accent/90"}`}
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
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, ease: "easeOut" }}
                className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                    m.role === "user"
                      ? "bg-accent text-ink rounded-br-sm shadow-lg shadow-accent/10"
                      : "bg-panel border border-line text-slate-200 rounded-bl-sm"
                  }`}
                >
                  {m.text}
                  {m.role === "agent" && m.sources && m.sources.length > 0 && (
                    <div className="mt-3 pt-2 border-t border-line/50 text-xs text-slate-400">
                      <div className="font-mono mb-1 text-slate-500">Fuentes:</div>
                      {m.sources.map((s, i) => (
                        <div key={i} className="text-slate-500 leading-relaxed">• {s}</div>
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
                <div className="flex gap-1 items-center">
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
          className="px-6 py-4 border-t border-line flex gap-3 bg-panel/30"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribí tu mensaje…"
            className="flex-1 bg-ink border border-line rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
          />
          <button
            type="submit"
            className="px-5 py-3 rounded-xl bg-accent text-ink font-medium hover:bg-accent/90 transition-colors shadow-lg shadow-accent/20"
          >
            Enviar
          </button>
        </form>
      </main>
    </div>
  );
}