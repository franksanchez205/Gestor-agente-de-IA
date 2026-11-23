"""Tests del canal de voz (STT/TTS)."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_voice_transcribe():
    r = client.post("/voice/transcribe", files={"audio": ("test.wav", b"fake audio", "audio/wav")})
    assert r.status_code == 200
    assert "text" in r.json()


def test_voice_speak():
    r = client.post("/voice/speak", params={"text": "hola"})
    assert r.status_code == 200
    assert "audio_url" in r.json()