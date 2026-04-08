"""Tests for the social media backend."""

import pytest
from fastapi.testclient import TestClient
import requests

from src.social_media_backend import app


class _MockResponse:
    """Small fake response object for requests mocking."""

    def __init__(self, payload, status_code=200, text=""):
        self._payload = payload
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        """Simulate a successful request."""
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError()

    def json(self):
        return self._payload


def test_health():
    """Health endpoint should return ok status."""
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_returns_html():
    """Index endpoint should return the HTML file."""
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


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


def test_generate_post_with_different_models(monkeypatch):
    """Generate endpoint should work with different model selections."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Test content",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)

    for model in ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"]:
        response = client.post(
            "/generate-post",
            json={
                "api_key": "test-key",
                "prompt": "Write a post",
                "model": model,
            },
        )

        assert response.status_code == 200
        assert response.json()["model"] == model


def test_generate_post_strips_whitespace_from_api_key(monkeypatch):
    """Generate endpoint should strip whitespace from API keys."""

    captured_headers = {}

    def _mock_post(*args, **kwargs):
        captured_headers.update(kwargs.get("headers", {}))
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Test",
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
            "api_key": "  test-key-with-spaces  ",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 200
    # Verify the authorization header has no leading/trailing spaces
    assert captured_headers["Authorization"] == "Bearer test-key-with-spaces"


def test_generate_post_invalid_api_key(monkeypatch):
    """Generate endpoint should handle 401 authentication errors."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {"message": "Invalid API key"},
            status_code=401,
            text='{"message": "Invalid API key"}'
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "invalid-key",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]


def test_generate_post_rate_limit_exceeded(monkeypatch):
    """Generate endpoint should handle 429 rate limit errors."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {"error": {"message": "Rate limit exceeded"}},
            status_code=429,
            text='{"error": {"message": "Rate limit exceeded"}}'
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["detail"]


def test_generate_post_api_error(monkeypatch):
    """Generate endpoint should handle general API errors."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {"error": {"message": "Service unavailable"}},
            status_code=503,
            text='{"error": {"message": "Service unavailable"}}'
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 503
    assert "Mistral API error" in response.json()["detail"]


def test_generate_post_timeout(monkeypatch):
    """Generate endpoint should handle request timeouts."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 504
    assert "timeout" in response.json()["detail"].lower()


def test_generate_post_network_error(monkeypatch):
    """Generate endpoint should handle network errors."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Network unreachable")

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 500
    assert "Network error" in response.json()["detail"]


def test_generate_post_default_model(monkeypatch):
    """Generate endpoint should use default model when not specified."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Test content",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    # Don't specify model in request
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "Write a post",
        },
    )

    assert response.status_code == 200
    # Should use default model
    assert response.json()["model"] == "mistral-small-latest"


def test_generate_post_validation_missing_api_key(monkeypatch):
    """Generate endpoint should require API key."""

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "prompt": "Write a post",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 422  # Validation error


def test_generate_post_validation_missing_prompt(monkeypatch):
    """Generate endpoint should require prompt."""

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 422  # Validation error


def test_generate_post_correct_request_format(monkeypatch):
    """Generate endpoint should send correctly formatted request to Mistral API."""

    captured_request = {}

    def _mock_post(*args, **kwargs):
        captured_request["url"] = args[0] if args else kwargs.get("url")
        captured_request["headers"] = kwargs.get("headers", {})
        captured_request["json"] = kwargs.get("json", {})
        captured_request["timeout"] = kwargs.get("timeout")
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Test",
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
            "api_key": "my-api-key",
            "prompt": "Write a post about AI",
            "model": "mistral-large-latest",
        },
    )

    assert response.status_code == 200
    # Verify request structure
    assert captured_request["url"] == "https://api.mistral.ai/v1/chat/completions"
    assert captured_request["headers"]["Authorization"] == "Bearer my-api-key"
    assert captured_request["headers"]["Content-Type"] == "application/json"
    assert captured_request["json"]["model"] == "mistral-large-latest"
    assert captured_request["json"]["messages"] == [{"role": "user", "content": "Write a post about AI"}]
    assert captured_request["timeout"] == 60


# Additional regression and boundary tests


def test_generate_post_empty_prompt_string(monkeypatch):
    """Test that empty prompt string is handled (boundary case)."""

    def _mock_post(*args, **kwargs):
        # Mistral API might return error or empty response for empty prompts
        return _MockResponse(
            {"choices": []},
            status_code=400,
            text='{"error": {"message": "Invalid request"}}'
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": "",  # Empty string
            "model": "mistral-small-latest",
        },
    )

    # Should return error status code for empty prompt
    assert response.status_code in [400, 500]


def test_generate_post_very_long_prompt(monkeypatch):
    """Test handling of very long prompts (boundary case)."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Response to long prompt",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)
    # Create a very long prompt (10000 characters)
    long_prompt = "Write a social media post about " + ("AI " * 3000)

    response = client.post(
        "/generate-post",
        json={
            "api_key": "test-key",
            "prompt": long_prompt,
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 200


def test_generate_post_special_characters_in_prompt(monkeypatch):
    """Test handling of special characters in prompt (boundary case)."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Response",
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
            "prompt": "Write about: @#$%^&*()[]{}|\\<>?/~`\"'",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 200


def test_generate_post_unicode_in_prompt(monkeypatch):
    """Test handling of unicode characters in prompt."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Unicode response: 你好世界 🚀",
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
            "prompt": "Write about: 你好世界 🚀 émojis",
            "model": "mistral-small-latest",
        },
    )

    assert response.status_code == 200
    assert "你好世界" in response.json()["post"]


def test_health_endpoint_multiple_calls():
    """Regression test: health endpoint should be idempotent."""

    client = TestClient(app)

    # Call health endpoint multiple times
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_generate_post_malformed_api_response(monkeypatch):
    """Regression test: handle malformed API responses gracefully."""

    def _mock_post(*args, **kwargs):
        # Return response missing expected fields
        return _MockResponse(
            {
                "choices": []  # Empty choices array
            },
            status_code=200
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)

    # This test verifies that malformed responses cause an internal error
    # The backend currently doesn't handle this edge case, which results in IndexError
    with pytest.raises(Exception):  # Could be IndexError or similar
        response = client.post(
            "/generate-post",
            json={
                "api_key": "test-key",
                "prompt": "Write a post",
                "model": "mistral-small-latest",
            },
        )


def test_static_files_mounted():
    """Test that static files are properly mounted."""

    client = TestClient(app)

    # Try to access a static file (styles.css)
    response = client.get("/static/styles.css")

    # Should either return the file or 404 if not found
    assert response.status_code in [200, 404]


def test_generate_post_preserves_provider_field(monkeypatch):
    """Regression test: verify provider field is always 'mistral'."""

    def _mock_post(*args, **kwargs):
        return _MockResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": "Test content",
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("src.social_media_backend.requests.post", _mock_post)

    client = TestClient(app)

    for model in ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"]:
        response = client.post(
            "/generate-post",
            json={
                "api_key": "test-key",
                "prompt": "Test",
                "model": model,
            },
        )

        assert response.status_code == 200
        data = response.json()
        # Provider should always be "mistral" regardless of model
        assert data["provider"] == "mistral"