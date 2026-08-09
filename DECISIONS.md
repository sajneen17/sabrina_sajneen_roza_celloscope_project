# Decisions

1. **Mock vs Real**: Defaulted to Mock to ensure zero-config startup. Real adapters can be switched via `.env`.
2. **Whisper for Real Transcription**: Chose OpenAI Whisper for its robust multi-language (bn/en) support. Rejected Google Cloud Speech due to cost and network dependency.
3. **Tesseract for OCR**: Chose open-source Tesseract. Rejected Azure Vision to avoid API key overhead.
4. **Normalization**: Chose to keep `<` and `>` prefixes, parse scientific notation to float, and preserve unparseable text verbatim to avoid hallucination (per requirement).
5. **File Validation**: Implemented both MIME type and extension check for reliability across browsers.
