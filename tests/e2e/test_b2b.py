"""Tests E2E del flujo B2B (ONG → beneficiario)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_b2b_full_flow():
    # 1. Registrar ONG
    r = client.post("/api/orgs/register", json={"name": "ONG E2E", "org_type": "ong", "contact_email": "e2e@ong.org"})
    assert r.status_code == 200
    org_id = r.json()["id"]

    # 2. Crear cupo para beneficiario
    r = client.post(f"/api/orgs/{org_id}/cupos", json={"beneficiary_email": "ben@e2e.com"})
    assert r.status_code == 200
    cupo_id = r.json()["id"]

    # 3. Verificar cupo
    r = client.get(f"/api/orgs/cupos/{cupo_id}")
    assert r.status_code == 200
    assert r.json()["beneficiary_email"] == "ben@e2e.com"

    # 4. Reporte de la ONG
    r = client.get(f"/api/orgs/{org_id}/report")
    assert r.status_code == 200
    assert r.json()["total_cupos"] == 1