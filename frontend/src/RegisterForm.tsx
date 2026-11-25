import { useState } from "react";
import { setToken, setUser } from "./auth";

export default function RegisterForm({ onRegister }: { onRegister: () => void }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nationality, setNationality] = useState("AR");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, nationality }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Error al registrar. Verificá los datos.");
        return;
      }
      setToken(data.access_token);
      setUser({ user_id: data.user_id });
      onRegister();
    } catch {
      setError("Error de conexión. Verificá tu conexión a internet.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink px-4">
      <form onSubmit={handleSubmit} className="bg-panel border border-line rounded-2xl p-8 w-full max-w-sm space-y-4" aria-labelledby="register-title">
        <h2 id="register-title" className="text-xl font-semibold text-center">Registrarse</h2>
        {error && <div role="alert" aria-live="polite" className="text-sm text-red-400">{error}</div>}
        <div className="space-y-1">
          <label htmlFor="reg-name" className="text-xs text-slate-400">Nombre</label>
          <input
            id="reg-name"
            name="name"
            autoComplete="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Tu nombre…"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
            required
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="reg-email" className="text-xs text-slate-400">Email</label>
          <input
            id="reg-email"
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
          <label htmlFor="reg-password" className="text-xs text-slate-400">Contraseña</label>
          <input
            id="reg-password"
            type="password"
            name="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
            required
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="reg-nationality" className="text-xs text-slate-400">Nacionalidad</label>
          <input
            id="reg-nationality"
            name="nationality"
            value={nationality}
            onChange={(e) => setNationality(e.target.value)}
            placeholder="AR, ES, …"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm disabled:opacity-50 hover:bg-accent/90 transition-colors focus-visible:ring-2 focus-visible:ring-accent"
        >
          {loading ? "Registrando…" : "Registrarse"}
        </button>
      </form>
    </div>
  );
}