import os
import tempfile
from app.adapters.transcription import get_transcriber
from app.api.schemas import TranscriptionResponse
from app.core.exceptions import ProcessingError

class TranscriptionService:
    def __init__(self):
        self.adapter = get_transcriber()

    async def transcribe(self, file_content: bytes, filename: str, language: str) -> TranscriptionResponse:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            result = await self.adapter.transcribe(tmp_path, language)
            return result
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
