"""Tests de integración de autenticación (register + login + me)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.data.database import get_db
from src.data.models import Base

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSession = sessionmaker(bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_register_login_me_flow(client):
    # Register
    r = client.post("/api/auth/register", json={"name": "Juan", "email": "juan@test.com", "password": "secret123", "nationality": "AR"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    # Login
    r = client.post("/api/auth/login", json={"email": "juan@test.com", "password": "secret123"})
    assert r.status_code == 200
    assert "access_token" in r.json()

    # Me (protegido)
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["user_id"] == "u-juan@test.com"


def test_login_invalid_credentials(client):
    client.post("/api/auth/register", json={"name": "Juan", "email": "juan@test.com", "password": "secret123"})
    r = client.post("/api/auth/login", json={"email": "juan@test.com", "password": "wrong"})
    assert r.status_code == 401


def test_me_without_token(client):
    r = client.get("/api/auth/me")
    assert r.status_code in (401, 403)  # HTTPBearer returns 401/403 when no credentials