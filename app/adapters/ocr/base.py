from abc import ABC, abstractmethod
from app.api.schemas import DocumentExtractResponse

class BaseOCR(ABC):
    @abstractmethod
    async def extract(self, file_path: str) -> DocumentExtractResponse:
        pass
