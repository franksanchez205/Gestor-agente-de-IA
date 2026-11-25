"""Punto de entrada de la aplicación FastAPI."""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.api.whatsapp import router as whatsapp_router
from src.api.voice import router as voice_router
from src.api.expediente import router as expediente_router
from src.api.credentials import router as credentials_router
from src.api.orgs import router as orgs_router
from src.api.auth import router as auth_router
from src.api.chat import router as chat_router

app = FastAPI(title="Puente", version="0.1.0")

app.include_router(whatsapp_router)
app.include_router(voice_router)
app.include_router(expediente_router)
app.include_router(credentials_router)
app.include_router(orgs_router)
app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/health")
async def health():
    return {"status": "ok"}