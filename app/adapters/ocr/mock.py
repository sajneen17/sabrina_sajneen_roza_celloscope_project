import json
import os
from app.adapters.ocr.base import BaseOCR
from app.api.schemas import DocumentExtractResponse

class MockOCR(BaseOCR):
    async def extract(self, file_path: str) -> DocumentExtractResponse:
        mock_file = os.path.join("testdata", "mock_ocr", "sample_report.json")
        if not os.path.exists(mock_file):
            # Fallback static
            return DocumentExtractResponse(
                meta={},
                results=[],
                provider="mock"
            )
        with open(mock_file, "r") as f:
            data = json.load(f)
        return DocumentExtractResponse(**data)
