import pytest
from fastapi.testclient import TestClient
from main import app
from services.google_auth import verify_google_token

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the e-bnk API"}

def test_apple_app_site_association():
    response = client.get("/.well-known/apple-app-site-association")
    assert response.status_code == 200
    assert "applinks" in response.json()

def test_verify_google_token_mock():
    # Test the mock logic for invalid token
    token = "invalid_token"
    result = verify_google_token(token)
    assert result is not None  # assuming we are still in mock mode where it returns a mock user or something
    assert result.get("email") == "mockuser@google.com"

# More tests can be added for actual authentication routes
