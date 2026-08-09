import os
import tempfile
import whisper
from app.adapters.transcription.base import BaseTranscriber
from app.api.schemas import TranscriptionResponse
from app.core.exceptions import ProcessingError

class RealWhisperTranscriber(BaseTranscriber):
    def __init__(self):
        # Model is loaded only when this class is instantiated (real adapter)
        self.model = whisper.load_model("base")

    async def transcribe(self, file_path: str, language: str) -> TranscriptionResponse:
        try:
            # Whisper expects language code like 'en', 'bn'. 'auto' passes None.
            lang = None if language == "auto" else language
            result = self.model.transcribe(file_path, language=lang)
            # Simple no-speech check (if result text is empty or very short)
            if not result["text"].strip():
                return TranscriptionResponse(
                    transcript="",
                    detected_language=result.get("language", "unknown"),
                    audio_duration=result.get("segments", [{}])[-1].get("end", 0) if result.get("segments") else 0,
                    provider="real_whisper"
                )
            return TranscriptionResponse(
                transcript=result["text"].strip(),
                detected_language=result.get("language", "unknown"),
                audio_duration=result.get("segments", [{}])[-1].get("end", 0) if result.get("segments") else 0,
                provider="real_whisper"
            )
        except Exception as e:
            raise ProcessingError(f"Whisper transcription failed: {str(e)}")
