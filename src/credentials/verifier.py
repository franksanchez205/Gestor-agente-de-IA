"""Verificador de credenciales verificables.

Envuelve la verificación de JWT-VC con validaciones adicionales:
- Firma válida
- No expirada
- Issuer esperado (opcional)
- Subject esperado (opcional)
"""

from typing import Any

from src.credentials.vc import verify_vc, VCError


class CredentialVerifier:
    def __init__(self, secret_key: str, expected_issuer: str | None = None):
        self.secret_key = secret_key
        self.expected_issuer = expected_issuer

    def verify(self, token: str, expected_subject: str | None = None) -> dict[str, Any]:
        """Verifica una credencial y valida campos opcionales.

        Raises:
            VCError: si la credencial es inválida, expiró, o no cumple validaciones.
        """
        payload = verify_vc(token, self.secret_key)

        if self.expected_issuer is not None and payload.get("issuer") != self.expected_issuer:
            raise VCError(f"Issuer inesperado: {payload.get('issuer')}")

        subject = payload.get("credentialSubject", {}).get("id")
        if expected_subject is not None and subject != expected_subject:
            raise VCError(f"Subject inesperado: {subject}")

        return payload

    def is_valid(self, token: str, expected_subject: str | None = None) -> bool:
        try:
            self.verify(token, expected_subject)
            return True
        except VCError:
            return False