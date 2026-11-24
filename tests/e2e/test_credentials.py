"""Tests E2E de credenciales verificables."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_issue_credential():
    r = client.post("/api/credentials/issue", json={"subject_did": "did:example:user1", "doc_type": "passport", "issued_by": "AR"})
    assert r.status_code == 200
    assert "token" in r.json()


def test_verify_credential():
    # Emitir
    r = client.post("/api/credentials/issue", json={"subject_did": "did:example:user1", "doc_type": "passport", "issued_by": "AR"})
    token = r.json()["token"]
    # Verificar
    r = client.post("/api/credentials/verify", json={"token": token})
    assert r.status_code == 200
    assert r.json()["valid"] is True


def test_verify_invalid_credential():
    r = client.post("/api/credentials/verify", json={"token": "invalid.token"})
    assert r.status_code == 200
    assert r.json()["valid"] is False