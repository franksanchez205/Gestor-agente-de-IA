"""Canal WhatsApp: webhook de entrada y envío de mensajes."""

from fastapi import APIRouter, Request

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    # Stub: procesar mensaje entrante y responder con el agente
    return {"status": "ok"}


@router.get("/webhook")
async def verify(request: Request):
    # Verificación del webhook de Meta
    return {"challenge": request.query_params.get("hub.challenge")}