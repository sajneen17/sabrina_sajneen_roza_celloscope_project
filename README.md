# Celloscope AI Service

## How to run
```bash
docker compose up
```
Service runs on `http://localhost:8000`.

## Architecture
- **API Layer**: FastAPI routes, validation, error handling.
- **Services Layer**: Orchestrates adapters, no FastAPI imports.
- **Adapters Layer**: Mock and Real providers (Whisper, Tesseract).

## Normalized Value Format
- Scientific notation (1.2 x 10^3) -> `1200.0`
- Ranges -> First value extracted.
- Unparseable -> preserved verbatim.

## Test Data
Collected from open-source datasets (LibriSpeech for audio, random lab reports from Kaggle). Chosen to include edge cases like tilted angles, noise, and silence.

## Known Limitations
- Real OCR parsing is dummy regex-based in this skeleton.
- Real Whisper requires `openai-whisper` and PyTorch (not included in default deps to keep mock light).
