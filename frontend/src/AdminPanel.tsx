import { useState } from "react";

type Org = { id: string; name: string; org_type: string; contact_email: string };
type Cupo = { id: string; beneficiary_email: string; used: boolean };
type Report = { org: Org; total_cupos: number; used_cupos: number; cupos: Cupo[] };

export default function AdminPanel() {
  const [orgs, setOrgs] = useState<Org[]>([]);
  const [selectedOrg, setSelectedOrg] = useState<string>("");
  const [report, setReport] = useState<Report | null>(null);
  const [newOrgName, setNewOrgName] = useState("");
  const [newOrgEmail, setNewOrgEmail] = useState("");
  const [beneficiaryEmail, setBeneficiaryEmail] = useState("");
  const [error, setError] = useState("");

  async function registerOrg() {
    if (!newOrgName || !newOrgEmail) {
      setError("Completá nombre y email.");
      return;
    }
    setError("");
    const res = await fetch("/api/orgs/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newOrgName, org_type: "ong", contact_email: newOrgEmail }),
    });
    const data = await res.json();
    if (!res.ok) {
      setError(data.error || "Error al registrar.");
      return;
    }
    setOrgs((o) => [...o, data]);
    setNewOrgName("");
    setNewOrgEmail("");
  }

  async function loadReport(orgId: string) {
    setSelectedOrg(orgId);
    const res = await fetch(`/api/orgs/${orgId}/report`);
    const data = await res.json();
    setReport(data);
  }

  async function createCupo() {
    if (!selectedOrg || !beneficiaryEmail) return;
    await fetch(`/api/orgs/${selectedOrg}/cupos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ beneficiary_email: beneficiaryEmail }),
    });
    setBeneficiaryEmail("");
    loadReport(selectedOrg);
  }

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-semibold">Panel de administración (B2B)</h2>

      {error && <div role="alert" aria-live="polite" className="text-sm text-red-400">{error}</div>}

      {/* Registrar ONG */}
      <div className="bg-panel border border-line rounded-xl p-4 space-y-3">
        <h3 className="font-medium text-sm text-slate-300">Registrar ONG</h3>
        <div className="space-y-1">
          <label htmlFor="org-name" className="text-xs text-slate-400">Nombre de la ONG</label>
          <input
            id="org-name"
            name="org_name"
            value={newOrgName}
            onChange={(e) => setNewOrgName(e.target.value)}
            placeholder="Cruz Roja…"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
          />
        </div>
        <div className="space-y-1">
          <label htmlFor="org-email" className="text-xs text-slate-400">Email de contacto</label>
          <input
            id="org-email"
            type="email"
            name="org_email"
            autoComplete="email"
            spellCheck={false}
            value={newOrgEmail}
            onChange={(e) => setNewOrgEmail(e.target.value)}
            placeholder="info@ong.org…"
            className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
          />
        </div>
        <button
          onClick={registerOrg}
          className="px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm hover:bg-accent/90 transition-colors focus-visible:ring-2 focus-visible:ring-accent"
        >
          Registrar
        </button>
      </div>

      {/* Lista de ONGs */}
      {orgs.length > 0 && (
        <div className="bg-panel border border-line rounded-xl p-4 space-y-2">
          <h3 className="font-medium text-sm text-slate-300">ONGs registradas</h3>
          {orgs.map((o) => (
            <button
              key={o.id}
              onClick={() => loadReport(o.id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${selectedOrg === o.id ? "bg-accent/20 text-accent" : "hover:bg-line/50"}`}
            >
              {o.name} ({o.org_type})
            </button>
          ))}
        </div>
      )}

      {/* Reporte */}
      {report && (
        <div className="bg-panel border border-line rounded-xl p-4 space-y-3">
          <h3 className="font-medium text-sm text-slate-300">Reporte: {report.org.name}</h3>
          <div className="flex gap-4 text-sm">
            <div>Total cupos: <span className="font-mono text-accent">{report.total_cupos}</span></div>
            <div>Usados: <span className="font-mono text-emerald-400">{report.used_cupos}</span></div>
          </div>
          <div className="space-y-2">
            <div className="space-y-1">
              <label htmlFor="beneficiary-email" className="text-xs text-slate-400">Email del beneficiario</label>
              <input
                id="beneficiary-email"
                type="email"
                name="beneficiary_email"
                autoComplete="email"
                spellCheck={false}
                value={beneficiaryEmail}
                onChange={(e) => setBeneficiaryEmail(e.target.value)}
                placeholder="ben@ejemplo.com…"
                className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent/30 transition-colors"
              />
            </div>
            <button
              onClick={createCupo}
              className="px-4 py-2 rounded-lg bg-emerald-500/20 text-emerald-400 font-medium text-sm hover:bg-emerald-500/30 transition-colors focus-visible:ring-2 focus-visible:ring-emerald-500"
            >
              Asignar cupo
            </button>
          </div>
          {report.cupos.length > 0 && (
            <div className="mt-2 space-y-1">
              {report.cupos.map((c) => (
                <div key={c.id} className="text-xs text-slate-400 flex justify-between">
                  <span>{c.beneficiary_email}</span>
                  <span className={c.used ? "text-emerald-400" : "text-amber-400"}>{c.used ? "usado" : "pendiente"}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}