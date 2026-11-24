"""API de verificación de credenciales verificables."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.credentials.verifier import CredentialVerifier

router = APIRouter(prefix="/api/credentials", tags=["credentials"])

# Clave de desarrollo (en producción se usa una clave asimétrica)
DEV_SECRET = "dev-secret-key"


class VerifyRequest(BaseModel):
    token: str
    expected_subject: str | None = None


@router.post("/verify")
async def verify_credential(req: VerifyRequest):
    verifier = CredentialVerifier(secret_key=DEV_SECRET)
    try:
        payload = verifier.verify(req.token, expected_subject=req.expected_subject)
        return {"valid": True, "payload": payload}
    except Exception as exc:
        return {"valid": False, "error": str(exc)}