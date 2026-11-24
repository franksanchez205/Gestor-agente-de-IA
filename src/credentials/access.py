"""Control de acceso a credenciales verificables.

Permite compartir (generar token de acceso temporal) y revocar credenciales.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from src.credentials.vc import VCError


class CredentialAccess:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self._shared: dict[str, dict[str, Any]] = {}  # share_token -> info

    def share(self, credential_id: str, expires_in_minutes: int = 60) -> str:
        """Genera un token de acceso temporal para compartir la credencial."""
        import uuid
        import jwt

        share_token = str(uuid.uuid4())
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        payload = {
            "share_token": share_token,
            "credential_id": credential_id,
            "exp": int(exp.timestamp()),
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        self._shared[share_token] = {
            "credential_id": credential_id,
            "expires_at": exp,
            "revoked": False,
        }
        return token

    def revoke_share(self, share_token: str) -> bool:
        """Revoca un token de acceso compartido."""
        if share_token in self._shared:
            self._shared[share_token]["revoked"] = True
            return True
        return False

    def check_access(self, share_token: str) -> bool:
        """Verifica si un token de acceso compartido es válido y no revocado."""
        info = self._shared.get(share_token)
        if info is None:
            return False
        if info["revoked"]:
            return False
        if datetime.now(timezone.utc) > info["expires_at"]:
            return False
        return True

    def revoke_credential(self, credential_id: str, revoked_set: set[str]) -> None:
        """Marca una credencial como revocada (agrega a un set de revocadas)."""
        revoked_set.add(credential_id)