"""Punto de entrada de la aplicación FastAPI."""

from fastapi import FastAPI
from src.api.whatsapp import router as whatsapp_router
from src.api.voice import router as voice_router
from src.api.expediente import router as expediente_router

app = FastAPI(title="Puente", version="0.1.0")

app.include_router(whatsapp_router)
app.include_router(voice_router)
app.include_router(expediente_router)


@app.get("/health")
async def health():
    return {"status": "ok"}