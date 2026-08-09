from fastapi import APIRouter
from app.api.routes import transcribe, extract

router = APIRouter()
router.include_router(transcribe.router, prefix="/api/v1", tags=["Transcription"])
router.include_router(extract.router, prefix="/api/v1", tags=["Extraction"])
