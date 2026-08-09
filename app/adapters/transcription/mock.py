import json
import os
from app.adapters.transcription.base import BaseTranscriber
from app.api.schemas import TranscriptionResponse
from app.core.exceptions import ProcessingError

class MockTranscriber(BaseTranscriber):
    async def transcribe(self, file_path: str, language: str) -> TranscriptionResponse:
        # Mock logic: read from a JSON file based on filename or just return static
        mock_file = os.path.join("testdata", "mock_transcriptions", "sample_en.json")
        if not os.path.exists(mock_file):
            # Fallback static response if file missing
            return TranscriptionResponse(
                transcript="This is a mock transcription.",
                detected_language="en",
                audio_duration=10.5,
                provider="mock"
            )
        with open(mock_file, "r") as f:
            data = json.load(f)
        return TranscriptionResponse(**data)
