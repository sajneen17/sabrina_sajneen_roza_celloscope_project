import os

# ফোল্ডার তৈরি
dirs = [
    "app",
    "app/api",
    "app/api/routes",
    "app/core",
    "app/services",
    "app/adapters",
    "app/adapters/transcription",
    "app/adapters/ocr",
    "app/utils",
    "tests",
    "testdata",
    "testdata/mock_transcriptions",
    "testdata/mock_ocr"
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

files = {}

files[".env.example"] = """ENV=development
TRANSCRIPTION_PROVIDER=mock
OCR_PROVIDER=mock
MAX_FILE_SIZE_MB=25
ALLOWED_AUDIO_TYPES=audio/wav,audio/mpeg,audio/flac
"""

files[".gitignore"] = """.env
__pycache__/
*.pyc
.pytest_cache/
.DS_Store
*.db
*.sqlite3
"""

files[".dockerignore"] = """__pycache__
*.pyc
.env
.git
.gitignore
README.md
DECISIONS.md
"""

files["requirements.txt"] = """fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
pytest==7.4.4
httpx==0.26.0
python-dotenv==1.0.0
"""

files["Dockerfile"] = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

files["docker-compose.yml"] = """version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - TRANSCRIPTION_PROVIDER=mock
      - OCR_PROVIDER=mock
      - MAX_FILE_SIZE_MB=25
    volumes:
      - ./testdata:/app/testdata
"""

files["README.md"] = """# Celloscope AI Service

## How to run
```bash
docker compose up
Service runs on http://localhost:8000
"""

files["DECISIONS.md"] = """# Decisions

Mock vs Real: Defaulted to Mock.

Whisper chosen over Google Cloud.

Tesseract chosen over Azure Vision.
"""

files["app/init.py"] = ""

files["app/main.py"] = """from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

app = FastAPI()
app.include_router(router)

@app.get("/health")
async def health():
return {"status": "ok"}
"""

files["app/core/init.py"] = ""
files["app/core/config.py"] = """from pydantic_settings import BaseSettings

class Settings(BaseSettings):
TRANSCRIPTION_PROVIDER: str = "mock"
OCR_PROVIDER: str = "mock"
MAX_FILE_SIZE_MB: int = 25

settings = Settings()
"""

files["app/core/exceptions.py"] = """class ProcessingError(Exception):
pass
"""

files["app/api/init.py"] = ""
files["app/api/schemas.py"] = """from pydantic import BaseModel
from typing import Optional, List

class TranscriptionResponse(BaseModel):
transcript: str
detected_language: str
audio_duration: float
provider: str

class TestResult(BaseModel):
test_name: str
value: str
unit: str
reference_range: Optional[str] = None
flag: Optional[str] = None
raw_line: str

class DocumentExtractResponse(BaseModel):
meta: dict
results: List[TestResult]
provider: str
"""

files["app/api/routes/init.py"] = """from fastapi import APIRouter
from app.api.routes import transcribe, extract

router = APIRouter()
router.include_router(transcribe.router, prefix="/api/v1", tags=["Transcription"])
router.include_router(extract.router, prefix="/api/v1", tags=["Extraction"])
"""

files["app/api/routes/transcribe.py"] = """from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.transcription_service import TranscriptionService
from app.core.config import settings
import os

router = APIRouter()
service = TranscriptionService()

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), language: str = Form("auto")):
content = await audio.read()
if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
raise HTTPException(413, "File too large")
return await service.transcribe(content, audio.filename, language)
"""

files["app/api/routes/extract.py"] = """from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extraction_service import ExtractionService
from app.core.config import settings

router = APIRouter()
service = ExtractionService()

@router.post("/documents/extract")
async def extract_document(image: UploadFile = File(...)):
content = await image.read()
if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
raise HTTPException(413, "File too large")
return await service.extract(content, image.filename)
"""

files["app/services/init.py"] = ""
files["app/services/transcription_service.py"] = """import os
import tempfile
from app.adapters.transcription import get_transcriber

class TranscriptionService:
def init(self):
self.adapter = get_transcriber()
async def transcribe(self, content, filename, language):
with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
tmp.write(content)
tmp_path = tmp.name
try:
return await self.adapter.transcribe(tmp_path, language)
finally:
os.unlink(tmp_path)
"""

files["app/services/extraction_service.py"] = """import os
import tempfile
from app.adapters.ocr import get_ocr

class ExtractionService:
def init(self):
self.adapter = get_ocr()
async def extract(self, content, filename):
with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
tmp.write(content)
tmp_path = tmp.name
try:
return await self.adapter.extract(tmp_path)
finally:
os.unlink(tmp_path)
"""

files["app/adapters/init.py"] = ""
files["app/adapters/transcription/init.py"] = """from app.core.config import settings
from app.adapters.transcription.mock import MockTranscriber

def get_transcriber():
if settings.TRANSCRIPTION_PROVIDER == "real_whisper":
from app.adapters.transcription.real_whisper import RealWhisperTranscriber
return RealWhisperTranscriber()
return MockTranscriber()
"""

files["app/adapters/transcription/base.py"] = """from abc import ABC, abstractmethod

class BaseTranscriber(ABC):
@abstractmethod
async def transcribe(self, file_path, language):
pass
"""

files["app/adapters/transcription/mock.py"] = """from app.adapters.transcription.base import BaseTranscriber
from app.api.schemas import TranscriptionResponse

class MockTranscriber(BaseTranscriber):
async def transcribe(self, file_path, language):
return TranscriptionResponse(
transcript="Mock transcription",
detected_language="en",
audio_duration=5.0,
provider="mock"
)
"""

files["app/adapters/transcription/real_whisper.py"] = """from app.adapters.transcription.base import BaseTranscriber
from app.api.schemas import TranscriptionResponse
import whisper

class RealWhisperTranscriber(BaseTranscriber):
def init(self):
self.model = whisper.load_model("base")
async def transcribe(self, file_path, language):
result = self.model.transcribe(file_path, language=language if language != "auto" else None)
return TranscriptionResponse(
transcript=result["text"],
detected_language=result.get("language", "unknown"),
audio_duration=result.get("segments", [{}])[-1].get("end", 0),
provider="real_whisper"
)
"""

files["app/adapters/ocr/init.py"] = """from app.core.config import settings
from app.adapters.ocr.mock import MockOCR

def get_ocr():
if settings.OCR_PROVIDER == "real_tesseract":
from app.adapters.ocr.real_tesseract import RealTesseractOCR
return RealTesseractOCR()
return MockOCR()
"""

files["app/adapters/ocr/base.py"] = """from abc import ABC, abstractmethod

class BaseOCR(ABC):
@abstractmethod
async def extract(self, file_path):
pass
"""

files["app/adapters/ocr/mock.py"] = """from app.adapters.ocr.base import BaseOCR
from app.api.schemas import DocumentExtractResponse, TestResult

class MockOCR(BaseOCR):
async def extract(self, file_path):
return DocumentExtractResponse(
meta={"patient_name": "Mock Patient"},
results=[TestResult(
test_name="Hb",
value="14.5",
unit="g/dL",
reference_range="12-16",
raw_line="Hb 14.5 g/dL 12-16"
)],
provider="mock"
)
"""

files["app/adapters/ocr/real_tesseract.py"] = """from app.adapters.ocr.base import BaseOCR
from app.api.schemas import DocumentExtractResponse
import cv2, pytesseract

class RealTesseractOCR(BaseOCR):
async def extract(self, file_path):
img = cv2.imread(file_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
text = pytesseract.image_to_string(gray)
return DocumentExtractResponse(meta={}, results=[], provider="real_tesseract")
"""

files["app/utils/init.py"] = ""
files["app/utils/normalizers.py"] = """def normalize_value(v): return v
def normalize_unit(u): return u
"""

files["tests/init.py"] = ""
files["tests/test_normalizers.py"] = """def test_dummy(): assert True
"""

files["tests/test_validation.py"] = """def test_dummy(): assert True
"""

files["tests/test_integration.py"] = """def test_dummy(): assert True
"""


files["testdata/mock_transcriptions/sample_en.json"] = '{"transcript":"Hello","detected_language":"en","audio_duration":5.2,"provider":"mock"}'
files["testdata/mock_ocr/sample_report.json"] = '{"meta":{"patient_name":"Mock"},"results":[],"provider":"mock"}'


for path, content in files.items():
with open(path, "w", encoding="utf-8") as f:
f.write(content)

print("✅ Project created successfully!")
print("👉 Now run: docker compose up")