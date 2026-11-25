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
        setError(data.detail || "Error al registrar");
        return;
      }
      setToken(data.access_token);
      setUser({ user_id: data.user_id });
      onRegister();
    } catch {
      setError("Error de conexión");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink">
      <form onSubmit={handleSubmit} className="bg-panel border border-line rounded-2xl p-8 w-full max-w-sm space-y-4">
        <h2 className="text-xl font-semibold text-center">Registrarse</h2>
        {error && <div className="text-sm text-red-400">{error}</div>}
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Nombre"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
          required
        />
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
        <input
          value={nationality}
          onChange={(e) => setNationality(e.target.value)}
          placeholder="Nacionalidad (AR, ES, ...)"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm disabled:opacity-50"
        >
          {loading ? "Registrando…" : "Registrarse"}
        </button>
      </form>
    </div>
  );
}