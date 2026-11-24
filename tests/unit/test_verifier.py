"""Tests unitarios del verificador de credenciales."""

import pytest
from src.credentials.vc import issue_vc
from src.credentials.verifier import CredentialVerifier, VCError

SECRET = "test-secret-key"


def test_verify_valid_credential():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    verifier = CredentialVerifier(secret_key=SECRET, expected_issuer="did:example:issuer")
    payload = verifier.verify(token, expected_subject="did:example:user1")
    assert payload["credentialSubject"]["doc_type"] == "passport"


def test_verify_wrong_issuer_raises():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    verifier = CredentialVerifier(secret_key=SECRET, expected_issuer="did:example:other")
    with pytest.raises(VCError, match="Issuer inesperado"):
        verifier.verify(token)


def test_verify_wrong_subject_raises():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    verifier = CredentialVerifier(secret_key=SECRET)
    with pytest.raises(VCError, match="Subject inesperado"):
        verifier.verify(token, expected_subject="did:example:other")


def test_is_valid_true():
    token = issue_vc(
        subject_did="did:example:user1",
        claims={"doc_type": "passport"},
        issuer_did="did:example:issuer",
        secret_key=SECRET,
    )
    verifier = CredentialVerifier(secret_key=SECRET)
    assert verifier.is_valid(token) is True


def test_is_valid_false():
    verifier = CredentialVerifier(secret_key=SECRET)
    assert verifier.is_valid("garbage") is False