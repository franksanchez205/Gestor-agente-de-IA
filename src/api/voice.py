"""Canal de voz: STT (speech-to-text) y TTS (text-to-speech)."""

from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    # Stub: convertir audio a texto
    return {"text": ""}


@router.post("/speak")
async def speak(text: str):
    # Stub: convertir texto a audio
    return {"audio_url": ""}