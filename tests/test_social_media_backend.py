"""Tests for the social media backend."""

from fastapi.testclient import TestClient

from src.social_media_backend import app


class _MockResponse:
    """Small fake response object for requests mocking."""

    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        """Simulate a successful request."""

    def json(self):
        return self._payload


def test_health():
    """Health endpoint should return ok status."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_post(monkeypatch):
    """Generate endpoint should return extracted post content."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Launch day update: we're shipping faster this week.",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write launch post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "post": "Launch day update: we're shipping faster this week.",
        "model": "mistral-small-latest",
        "provider": "mistral",
    }
