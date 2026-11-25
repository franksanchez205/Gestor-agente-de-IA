import { useState } from "react";
import { setToken, setUser } from "./auth";

export default function LoginForm({ onLogin }: { onLogin: () => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Error al iniciar sesión. Verificá tus credenciales.");
        return;
      }
      setToken(data.access_token);
      setUser({ user_id: data.user_id });
      onLogin();
    } catch {
      setError("Error de conexión. Verificá tu conexión a internet.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink px-4">
      <form onSubmit={handleSubmit} className="bg-panel border border-line rounded-2xl p-8 w-full max-w-sm space-y-4" aria-labelledby="login-title">
        <h2 id="login-title" className="text-xl font-semibold text-center">Iniciar sesión</h2>
        {error && <div role="alert" aria-live="polite" className="text-sm text-red-400">{error}</div>}
        <div className="space-y-1">
          <label htmlFor="login-email" className="text-xs text-slate-400">Email</label>
          <input
            id="login-email"
            type="email"
            name="email"
            autoComplete="email"
            spellCheck={false}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="tu@email.com…"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
            required
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="login-password" className="text-xs text-slate-400">Contraseña</label>
          <input
            id="login-password"
            type="password"
            name="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
            required
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm disabled:opacity-50 hover:bg-accent/90 transition-colors focus-visible:ring-2 focus-visible:ring-accent"
        >
          {loading ? "Iniciando…" : "Iniciar sesión"}
        </button>
      </form>
    </div>
  );
}