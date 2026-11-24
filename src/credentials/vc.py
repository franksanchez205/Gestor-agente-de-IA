"""Emisión y verificación de W3C Verifiable Credentials (JWT-VC).

Usa PyJWT para firmar/verificar. En producción se usa RS256 con claves
asimétricas; para desarrollo/tests se usa HS256 con una clave compartida.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

VC_TYPE = "VerifiableCredential"
VC_CONTEXT = "https://www.w3.org/2018/credentials/v1"


class VCError(Exception):
    """Error de credencial verificable."""


def issue_vc(
    subject_did: str,
    claims: dict[str, Any],
    issuer_did: str,
    secret_key: str,
    expires_in_days: int = 365,
    algorithm: str = "HS256",
) -> str:
    """Emite una Verifiable Credential como JWT (JWT-VC).

    Args:
        subject_did: DID del sujeto (el dueño del documento).
        claims: claims del documento (doc_type, issued_by, etc.).
        issuer_did: DID del emisor (la autoridad que emite).
        secret_key: clave para firmar.
        expires_in_days: días de validez.
        algorithm: algoritmo de firma (HS256 por defecto).

    Returns:
        JWT string (la credencial verificable).
    """
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=expires_in_days)
    payload = {
        "@context": VC_CONTEXT,
        "type": [VC_TYPE],
        "issuer": issuer_did,
        "issuanceDate": now.isoformat(),
        "expirationDate": exp.isoformat(),
        "exp": int(exp.timestamp()),
        "credentialSubject": {
            "id": subject_did,
            **claims,
        },
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_vc(
    token: str,
    secret_key: str,
    algorithms: list[str] | None = None,
) -> dict[str, Any]:
    """Verifica una Verifiable Credential (JWT-VC).

    Args:
        token: JWT string de la credencial.
        secret_key: clave para verificar la firma.
        algorithms: algoritmos aceptados.

    Returns:
        El payload verificado (claims).

    Raises:
        VCError: si la firma es inválida, expiró, o el token es malformado.
    """
    if algorithms is None:
        algorithms = ["HS256"]
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
    except jwt.ExpiredSignatureError:
        raise VCError("La credencial ha expirado.")
    except jwt.InvalidTokenError as exc:
        raise VCError(f"Credencial inválida: {exc}")

    # Validar campos mínimos de VC
    if "credentialSubject" not in payload:
        raise VCError("Falta credentialSubject.")
    if "issuer" not in payload:
        raise VCError("Falta issuer.")

    return payload


def is_vc_valid(token: str, secret_key: str) -> bool:
    """Retorna True si la credencial es válida, False en caso contrario."""
    try:
        verify_vc(token, secret_key)
        return True
    except VCError:
        return False