"""API de expediente digital del cliente."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/expediente", tags=["expediente"])


@router.get("/")
async def get_expediente():
    # Stub: en producción se carga desde la BD usando el usuario autenticado
    return {
        "documents": [
            {"doc_type": "passport", "status": "valido", "expires": "2028-03-15"},
            {"doc_type": "permit", "status": "vence 30d", "expires": "2026-12-22"},
            {"doc_type": "title", "status": "apostillado", "expires": None},
        ],
        "notifications": [
            {"text": "Tu permiso de residencia vence en 30 días. ¿Gestiono la renovación?"},
        ],
    }