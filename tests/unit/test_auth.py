"""Tests unitarios de autenticación."""

import pytest
from src.auth.password import hash_password, verify_password
from src.auth.jwt import create_access_token, decode_access_token


def test_hash_and_verify_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_and_decode_access_token():
    token = create_access_token({"sub": "user-1"})
    payload = decode_access_token(token)
    assert payload["sub"] == "user-1"


def test_decode_invalid_token_raises():
    with pytest.raises(ValueError):
        decode_access_token("invalid.token.here")


def test_decode_expired_token_raises():
    from datetime import timedelta
    token = create_access_token({"sub": "user-1"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(ValueError, match="expirado"):
        decode_access_token(token)