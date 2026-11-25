import { useState } from "react";

export default function BeneficiaryActivation({ onActivated }: { onActivated: () => void }) {
  const [cupoId, setCupoId] = useState("");
  const [status, setStatus] = useState("");

  async function activate() {
    const res = await fetch(`/api/orgs/cupos/${cupoId}`);
    const data = await res.json();
    if (data.error) {
      setStatus("Cupo no encontrado. Verificá el ID.");
      return;
    }
    setStatus(`Cupo válido para ${data.beneficiary_email}. ¡Bienvenido a Puente!`);
    onActivated();
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-xl font-semibold">Activar cupo de ONG</h2>
      <p className="text-sm text-slate-400">Ingresá el ID de tu cupo asignado por la ONG.</p>
      <div className="space-y-1">
        <label htmlFor="cupo-id" className="text-xs text-slate-400">ID del cupo</label>
        <input
          id="cupo-id"
          name="cupo_id"
          value={cupoId}
          onChange={(e) => setCupoId(e.target.value)}
          placeholder="abc-123…"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
        />
      </div>
      <button
        onClick={activate}
        className="px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm hover:bg-accent/90 transition-colors focus-visible:ring-2 focus-visible:ring-accent"
      >
        Activar
      </button>
      {status && <div role="status" aria-live="polite" className="text-sm text-slate-300">{status}</div>}
    </div>
  );
}