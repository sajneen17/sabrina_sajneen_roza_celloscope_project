from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class TranscriptionResponse(BaseModel):
    transcript: str
    detected_language: str
    audio_duration: float
    provider: str

class ErrorResponse(BaseModel):
    detail: str
    code: str

class MetaData(BaseModel):
    patient_name: Optional[str] = None
    age: Optional[str] = None
    sex: Optional[str] = None
    report_date: Optional[str] = None
    lab_name: Optional[str] = None
    reference_no: Optional[str] = None

class TestResult(BaseModel):
    test_name: str
    value: str          # Normalized canonical string
    unit: str
    reference_range: Optional[str] = None
    flag: Optional[str] = None
    raw_line: str       # Original OCR line, NEVER cleaned

class DocumentExtractResponse(BaseModel):
    meta: MetaData
    results: List[TestResult]
    provider: str
