"""API de B2B: ONG y organismos de cooperación."""

import uuid
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/orgs", tags=["orgs"])

# In-memory store (stub; en producción se usa la BD)
_orgs: dict[str, dict] = {}
_cupos: dict[str, dict] = {}


class OrgRegisterRequest(BaseModel):
    name: str
    org_type: str  # ong | organism
    contact_email: str


class CupoAssignRequest(BaseModel):
    beneficiary_email: str


@router.post("/register")
async def register_org(req: OrgRegisterRequest):
    org_id = str(uuid.uuid4())
    org = {
        "id": org_id,
        "name": req.name,
        "org_type": req.org_type,
        "contact_email": req.contact_email,
    }
    _orgs[org_id] = org
    return org


@router.get("/{org_id}")
async def get_org(org_id: str):
    org = _orgs.get(org_id)
    if org is None:
        return {"error": "not found"}
    return org


@router.post("/{org_id}/cupos")
async def create_cupo(org_id: str, req: CupoAssignRequest):
    org = _orgs.get(org_id)
    if org is None:
        return {"error": "org not found"}
    cupo_id = str(uuid.uuid4())
    cupo = {
        "id": cupo_id,
        "org_id": org_id,
        "beneficiary_email": req.beneficiary_email,
        "assigned_at": None,
        "used": False,
        "used_at": None,
    }
    _cupos[cupo_id] = cupo
    return cupo


@router.get("/{org_id}/report")
async def org_report(org_id: str):
    org = _orgs.get(org_id)
    if org is None:
        return {"error": "org not found"}
    cupos = [c for c in _cupos.values() if c["org_id"] == org_id]
    return {
        "org": org,
        "total_cupos": len(cupos),
        "used_cupos": sum(1 for c in cupos if c["used"]),
        "cupos": cupos,
    }


@router.get("/cupos/{cupo_id}")
async def get_cupo(cupo_id: str):
    cupo = _cupos.get(cupo_id)
    if cupo is None:
        return {"error": "not found"}
    return cupo