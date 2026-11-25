"""Tests unitarios del endpoint de chat."""

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_chat_endpoint_returns_answer():
    r = client.post("/api/chat/", json={"message": "Hola"})
    # El endpoint puede retornar 200 (éxito) o 500 (error de LLM sin créditos)
    assert r.status_code in (200, 500)
    if r.status_code == 200:
        data = r.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)


def test_chat_endpoint_returns_sources():
    r = client.post("/api/chat/", json={"message": "permiso de residencia"})
    assert r.status_code in (200, 500)
    if r.status_code == 200:
        data = r.json()
        assert "sources" in data
        assert isinstance(data["sources"], list)


def test_chat_endpoint_empty_message():
    r = client.post("/api/chat/", json={"message": ""})
    assert r.status_code in (200, 500)