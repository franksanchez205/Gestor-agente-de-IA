"""Tests unitarios del control de acceso a credenciales."""

import pytest
from src.credentials.access import CredentialAccess


SECRET = "test-secret"


def test_share_generates_token():
    access = CredentialAccess(secret_key=SECRET)
    token = access.share(credential_id="cred-1", expires_in_minutes=30)
    assert isinstance(token, str)
    assert len(token) > 0


def test_check_access_valid():
    access = CredentialAccess(secret_key=SECRET)
    token = access.share(credential_id="cred-1", expires_in_minutes=30)
    # Extraer share_token del JWT
    import jwt
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    share_token = payload["share_token"]
    assert access.check_access(share_token) is True


def test_revoke_share_invalidates_access():
    access = CredentialAccess(secret_key=SECRET)
    token = access.share(credential_id="cred-1", expires_in_minutes=30)
    import jwt
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    share_token = payload["share_token"]
    assert access.revoke_share(share_token) is True
    assert access.check_access(share_token) is False


def test_check_access_unknown_token():
    access = CredentialAccess(secret_key=SECRET)
    assert access.check_access("unknown-token") is False


def test_revoke_share_unknown_returns_false():
    access = CredentialAccess(secret_key=SECRET)
    assert access.revoke_share("unknown-token") is False