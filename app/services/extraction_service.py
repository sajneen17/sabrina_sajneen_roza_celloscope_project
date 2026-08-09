import os
import tempfile
from app.adapters.ocr import get_ocr
from app.api.schemas import DocumentExtractResponse

class ExtractionService:
    def __init__(self):
        self.adapter = get_ocr()

    async def extract(self, file_content: bytes, filename: str) -> DocumentExtractResponse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            result = await self.adapter.extract(tmp_path)
            return result
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
