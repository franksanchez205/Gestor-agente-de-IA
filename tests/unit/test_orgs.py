"""Tests de la API B2B (ONG y organismos)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_register_org():
    r = client.post("/api/orgs/register", json={"name": "Cruz Roja", "org_type": "ong", "contact_email": "info@cruzroja.org"})
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Cruz Roja"
    assert "id" in data


def test_create_cupo():
    # Registrar org
    r = client.post("/api/orgs/register", json={"name": "ONG Test", "org_type": "ong", "contact_email": "test@ong.org"})
    org_id = r.json()["id"]
    # Crear cupo
    r = client.post(f"/api/orgs/{org_id}/cupos", json={"beneficiary_email": "ben@test.com"})
    assert r.status_code == 200
    data = r.json()
    assert data["beneficiary_email"] == "ben@test.com"
    assert data["used"] is False


def test_org_report():
    r = client.post("/api/orgs/register", json={"name": "ONG Report", "org_type": "ong", "contact_email": "report@ong.org"})
    org_id = r.json()["id"]
    client.post(f"/api/orgs/{org_id}/cupos", json={"beneficiary_email": "a@test.com"})
    client.post(f"/api/orgs/{org_id}/cupos", json={"beneficiary_email": "b@test.com"})
    r = client.get(f"/api/orgs/{org_id}/report")
    assert r.status_code == 200
    data = r.json()
    assert data["total_cupos"] == 2
    assert data["used_cupos"] == 0


def test_get_cupo():
    r = client.post("/api/orgs/register", json={"name": "ONG Cupo", "org_type": "ong", "contact_email": "cupo@ong.org"})
    org_id = r.json()["id"]
    r = client.post(f"/api/orgs/{org_id}/cupos", json={"beneficiary_email": "x@test.com"})
    cupo_id = r.json()["id"]
    r = client.get(f"/api/orgs/cupos/{cupo_id}")
    assert r.status_code == 200
    assert r.json()["beneficiary_email"] == "x@test.com"


def test_get_unknown_org():
    r = client.get("/api/orgs/nonexistent")
    assert r.status_code == 200
    assert "error" in r.json()