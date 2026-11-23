"""Tests end-to-end del flujo completo (WhatsApp → agente → resultado)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_full_flow_health_and_webhook():
    # 1. Health check
    r = client.get("/health")
    assert r.status_code == 200

    # 2. Cliente envía mensaje por WhatsApp
    r = client.post("/whatsapp/webhook", json={"message": "Necesito renovar mi permiso"})
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

    # 3. Verificación del webhook
    r = client.get("/whatsapp/webhook", params={"hub.challenge": "abc"})
    assert r.status_code == 200


def test_full_flow_voice():
    # 1. Transcribir audio
    r = client.post("/voice/transcribe", files={"audio": ("a.wav", b"audio", "audio/wav")})
    assert r.status_code == 200

    # 2. Generar respuesta por voz
    r = client.post("/voice/speak", params={"text": "Tu permiso vence en 30 días"})
    assert r.status_code == 200