import os
import cv2
import pytesseract
from app.adapters.ocr.base import BaseOCR
from app.api.schemas import DocumentExtractResponse, MetaData, TestResult
from app.core.exceptions import ProcessingError
from app.utils.normalizers import normalize_value, normalize_unit, extract_meta

class RealTesseractOCR(BaseOCR):
    async def extract(self, file_path: str) -> DocumentExtractResponse:
        try:
            # Read image
            img = cv2.imread(file_path)
            if img is None:
                raise ProcessingError("Could not read image file.")

            # Preprocess (grayscale, threshold)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # OCR
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(gray, config=custom_config)
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            # Dummy parsing for demo - In real scenario, you'd have sophisticated regex/rule parser
            meta = extract_meta(lines)  # You need to implement this regex parser
            results = []
            for line in lines:
                # Dummy parse: assume "Test Value Unit Range"
                parts = line.split()
                if len(parts) >= 4:
                    raw_line = line
                    test_name = parts[0]
                    value_raw = parts[1]
                    unit_raw = parts[2]
                    ref_range = " ".join(parts[3:])
                    norm_val = normalize_value(value_raw)
                    norm_unit = normalize_unit(unit_raw)
                    results.append(TestResult(
                        test_name=test_name,
                        value=norm_val,
                        unit=norm_unit,
                        reference_range=ref_range,
                        raw_line=raw_line
                    ))

            # If no results found, treat as non-lab-report gracefully
            if not results:
                return DocumentExtractResponse(meta=MetaData(), results=[], provider="real_tesseract")

            return DocumentExtractResponse(
                meta=meta,
                results=results,
                provider="real_tesseract"
            )
        except Exception as e:
            raise ProcessingError(f"Tesseract extraction failed: {str(e)}")
