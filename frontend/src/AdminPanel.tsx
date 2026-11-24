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

  async function registerOrg() {
    if (!newOrgName || !newOrgEmail) return;
    const res = await fetch("/api/orgs/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newOrgName, org_type: "ong", contact_email: newOrgEmail }),
    });
    const data = await res.json();
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

      {/* Registrar ONG */}
      <div className="bg-panel border border-line rounded-xl p-4 space-y-3">
        <h3 className="font-medium text-sm text-slate-300">Registrar ONG</h3>
        <input
          value={newOrgName}
          onChange={(e) => setNewOrgName(e.target.value)}
          placeholder="Nombre de la ONG"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
        />
        <input
          value={newOrgEmail}
          onChange={(e) => setNewOrgEmail(e.target.value)}
          placeholder="Email de contacto"
          className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
        />
        <button onClick={registerOrg} className="px-4 py-2 rounded-lg bg-accent text-ink font-medium text-sm">
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
              className={`w-full text-left px-3 py-2 rounded-lg text-sm ${selectedOrg === o.id ? "bg-accent/20 text-accent" : "hover:bg-line/50"}`}
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
            <div>Usados: <span className="font-mono text-ok">{report.used_cupos}</span></div>
          </div>
          <div className="space-y-2">
            <input
              value={beneficiaryEmail}
              onChange={(e) => setBeneficiaryEmail(e.target.value)}
              placeholder="Email del beneficiario"
              className="w-full bg-ink border border-line rounded-lg px-3 py-2 text-sm"
            />
            <button onClick={createCupo} className="px-4 py-2 rounded-lg bg-ok/20 text-ok font-medium text-sm">
              Asignar cupo
            </button>
          </div>
          {report.cupos.length > 0 && (
            <div className="mt-2 space-y-1">
              {report.cupos.map((c) => (
                <div key={c.id} className="text-xs text-slate-400 flex justify-between">
                  <span>{c.beneficiary_email}</span>
                  <span className={c.used ? "text-ok" : "text-warn"}>{c.used ? "usado" : "pendiente"}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}