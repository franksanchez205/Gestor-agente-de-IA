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
        setError(data.detail || "Error al iniciar sesión");
        return;
      }
      setToken(data.access_token);
      setUser({ user_id: data.user_id });
      onLogin();
    } catch {
      setError("Error de conexión");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink">
      <form onSubmit={handleSubmit} className="bg-panel border border-line rounded-2xl p-8 w-full max-w-sm space-y-4">
        <h2 className="text-xl font-semibold text-center">Iniciar sesión</h2>
        {error && <div className="text-sm text-red-400">{error}</div>}
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Contraseña"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm disabled:opacity-50"
        >
          {loading ? "Iniciando…" : "Iniciar sesión"}
        </button>
      </form>
    </div>
  );
}