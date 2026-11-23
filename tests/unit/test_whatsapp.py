"""Tests del canal WhatsApp (webhook)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_whatsapp_webhook_post():
    r = client.post("/whatsapp/webhook", json={"message": "hola"})
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_whatsapp_webhook_verify():
    r = client.get("/whatsapp/webhook", params={"hub.challenge": "12345"})
    assert r.status_code == 200
    assert r.json() == {"challenge": "12345"}