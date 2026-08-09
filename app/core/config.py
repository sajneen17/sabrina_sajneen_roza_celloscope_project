from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Celloscope AI Service"
    ENV: str = "development"
    TRANSCRIPTION_PROVIDER: str = "mock"
    OCR_PROVIDER: str = "mock"
    MAX_FILE_SIZE_MB: int = 25
    ALLOWED_AUDIO_TYPES: List[str] = ["audio/wav", "audio/mpeg", "audio/flac"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
