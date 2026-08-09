import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_audio_format():
    # Sending text file as audio
    with open("tests/__init__.py", "rb") as f:
        response = client.post("/api/v1/transcribe", files={"audio": ("test.txt", f, "text/plain")}, data={"language": "en"})
    assert response.status_code == 400
