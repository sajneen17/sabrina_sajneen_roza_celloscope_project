from abc import ABC, abstractmethod
from app.api.schemas import TranscriptionResponse

class BaseTranscriber(ABC):
    @abstractmethod
    async def transcribe(self, file_path: str, language: str) -> TranscriptionResponse:
        pass
