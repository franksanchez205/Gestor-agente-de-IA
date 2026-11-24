"""Tests unitarios de credenciales verificables (JWT-VC)."""

import pytest
from src.credentials.vc import issue_vc, verify_vc, is_vc_valid, VCError

SECRET = "test-secret-key"


def test_issue_and_verify_roundtrip():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport", "issued_by": "AR"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    payload = verify_vc(token, SECRET)
    assert payload["issuer"] == "did:example:issuer"
    assert payload["credentialSubject"]["id"] == "did:example:user1"
    assert payload["credentialSubject"]["doc_type"] == "passport"


def test_verify_invalid_token_raises():
    with pytest.raises(VCError):
        verify_vc("invalid.token.here", SECRET)


def test_verify_wrong_key_raises():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    with pytest.raises(VCError):
        verify_vc(token, "wrong-key")


def test_is_vc_valid_true():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    assert is_vc_valid(token, SECRET) is True


def test_is_vc_valid_false():
    assert is_vc_valid("garbage", SECRET) is False


def test_expired_vc_raises():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
        expires_in_days=-1,
    )
    with pytest.raises(VCError, match="expirado"):
        verify_vc(token, SECRET)