"""API de verificación de credenciales verificables."""

from fastapi import APIRouter
from pydantic import BaseModel

from src.credentials.vc import issue_vc
from src.credentials.verifier import CredentialVerifier

router = APIRouter(prefix="/api/credentials", tags=["credentials"])

# Clave de desarrollo (en producción se usa una clave asimétrica)
DEV_SECRET = "dev-secret-key"
DEV_ISSUER = "did:example:puente"


class VerifyRequest(BaseModel):
    token: str
    expected_subject: str | None = None


class IssueRequest(BaseModel):
    subject_did: str
    doc_type: str
    issued_by: str


@router.post("/verify")
async def verify_credential(req: VerifyRequest):
    verifier = CredentialVerifier(secret_key=DEV_SECRET)
    try:
        payload = verifier.verify(req.token, expected_subject=req.expected_subject)
        return {"valid": True, "payload": payload}
    except Exception as exc:
        return {"valid": False, "error": str(exc)}


@router.post("/issue")
async def issue_credential(req: IssueRequest):
    token = issue_vc(
        subject_did=req.subject_did,
        claims={"doc_type": req.doc_type, "issued_by": req.issued_by},
        issuer_did=DEV_ISSUER,
        secret_key=DEV_SECRET,
    )
    return {"token": token, "issuer": DEV_ISSUER}