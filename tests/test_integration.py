import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_transcribe_mock():
    dummy_audio = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"  # minimal header
    response = client.post("/api/v1/transcribe", files={"audio": ("test.wav", dummy_audio, "audio/wav")}, data={"language": "en"})
    assert response.status_code == 200
    assert response.json()["provider"] == "mock"

def test_extract_mock():
    dummy_img = b"dummy_image_data"
    response = client.post("/api/v1/documents/extract", files={"image": ("test.jpg", dummy_img, "image/jpeg")})
    assert response.status_code == 200
    assert response.json()["provider"] == "mock"
