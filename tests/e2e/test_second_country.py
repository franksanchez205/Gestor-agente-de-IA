"""Tests E2E del flujo en un segundo país (España)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_flow_second_country_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_flow_second_country_webhook():
    r = client.post("/whatsapp/webhook", json={"message": "Necesito apostillar mi título para España"})
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_flow_second_country_voice():
    r = client.post("/voice/transcribe", files={"audio": ("a.wav", b"audio", "audio/wav")})
    assert r.status_code == 200
    r = client.post("/voice/speak", params={"text": "Tu título será apostillado para España"})
    assert r.status_code == 200