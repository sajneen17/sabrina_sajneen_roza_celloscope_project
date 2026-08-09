from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.schemas import DocumentExtractResponse, ErrorResponse
from app.services.extraction_service import ExtractionService
from app.core.config import settings
import os

router = APIRouter()
service = ExtractionService()

@router.post("/documents/extract", response_model=DocumentExtractResponse, responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}})
async def extract_document(
    image: UploadFile = File(...)
):
    content = await image.read()
    file_size_mb = len(content) / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB."
        )

    # Accept common image types
    if image.content_type not in ["image/jpeg", "image/png", "image/tiff"]:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.tiff']:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Allowed: JPEG, PNG, TIFF."
            )

    try:
        result = await service.extract(content, image.filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
