from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.api.schemas import TranscriptionResponse, ErrorResponse
from app.services.transcription_service import TranscriptionService
from app.core.config import settings
import os

router = APIRouter()
service = TranscriptionService()

@router.post("/transcribe", response_model=TranscriptionResponse, responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}})
async def transcribe_audio(
    audio: UploadFile = File(...),
    language: str = Form("auto")
):
    # 1. Validation: File size
    content = await audio.read()
    file_size_mb = len(content) / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB."
        )

    # 2. Validation: MIME type (check extension as fallback)
    if audio.content_type not in settings.ALLOWED_AUDIO_TYPES:
        # fallback to extension check
        ext = os.path.splitext(audio.filename)[1].lower()
        allowed_exts = ['.wav', '.mp3', '.flac']
        if ext not in allowed_exts:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {settings.ALLOWED_AUDIO_TYPES}"
            )

    # 3. Call service (no FastAPI types passed to service)
    try:
        result = await service.transcribe(content, audio.filename, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
