"""Tests for the test_api_key.py script."""

import pytest
import requests
from unittest.mock import MagicMock, patch
import sys
from io import StringIO

from test_api_key import validate_mistral_key


class MockResponse:
    """Mock response for requests."""

    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text

    def json(self):
        return self._json_data


def test_validate_mistral_key_success(monkeypatch, capsys):
    """Test successful API key validation."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("valid-test-api-key-12345678")

    captured = capsys.readouterr()
    assert "✅ SUCCESS!" in captured.out
    assert "valid and working" in captured.out
    assert "hello" in captured.out


def test_validate_mistral_key_strips_whitespace(monkeypatch, capsys):
    """Test that API key whitespace is stripped."""

    captured_key = {}

    def _mock_post(*args, **kwargs):
        headers = kwargs.get("headers", {})
        auth_header = headers.get("Authorization", "")
        captured_key["auth"] = auth_header
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("  valid-key-with-spaces  ")

    # Verify whitespace was stripped
    assert captured_key["auth"] == "Bearer valid-key-with-spaces"


def test_validate_mistral_key_preview_format(monkeypatch, capsys):
    """Test that API key preview is formatted correctly."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("abcd1234efgh5678")

    captured = capsys.readouterr()
    assert "Preview: abcd...5678" in captured.out
    assert "Length: 16 characters" in captured.out


def test_validate_mistral_key_short_key(monkeypatch, capsys):
    """Test handling of very short API keys."""

    def _mock_post(*args, **kwargs):
        return MockResponse(status_code=401, text='{"message": "Invalid key"}')

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("short")

    captured = capsys.readouterr()
    assert "Key too short!" in captured.out


def test_validate_mistral_key_401_error(monkeypatch, capsys):
    """Test handling of 401 authentication errors."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=401,
            text='{"message": "Invalid authentication token"}'
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("invalid-key-12345678")

    captured = capsys.readouterr()
    assert "❌ AUTHENTICATION FAILED" in captured.out
    assert "API key is incorrect or expired" in captured.out
    assert "https://console.mistral.ai/" in captured.out


def test_validate_mistral_key_unexpected_status(monkeypatch, capsys):
    """Test handling of unexpected status codes."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=503,
            text='{"error": "Service temporarily unavailable"}'
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key-12345678")

    captured = capsys.readouterr()
    assert "⚠️  Unexpected response: 503" in captured.out
    assert "Service temporarily unavailable" in captured.out


def test_validate_mistral_key_network_error(monkeypatch, capsys):
    """Test handling of network errors."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("Connection refused")

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key-12345678")

    captured = capsys.readouterr()
    assert "❌ Network error:" in captured.out
    assert "Connection refused" in captured.out
    assert "Check your internet connection" in captured.out


def test_validate_mistral_key_timeout_error(monkeypatch, capsys):
    """Test handling of timeout errors."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key-12345678")

    captured = capsys.readouterr()
    assert "❌ Network error:" in captured.out
    assert "Request timed out" in captured.out


def test_validate_mistral_key_request_parameters(monkeypatch):
    """Test that the request is made with correct parameters."""

    captured_request = {}

    def _mock_post(*args, **kwargs):
        captured_request["url"] = args[0] if args else kwargs.get("url")
        captured_request["headers"] = kwargs.get("headers", {})
        captured_request["json"] = kwargs.get("json", {})
        captured_request["timeout"] = kwargs.get("timeout")
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("my-test-key-123")

    # Verify request parameters
    assert captured_request["url"] == "https://api.mistral.ai/v1/chat/completions"
    assert captured_request["headers"]["Authorization"] == "Bearer my-test-key-123"
    assert captured_request["headers"]["Content-Type"] == "application/json"
    assert captured_request["json"]["model"] == "mistral-small-latest"
    assert captured_request["json"]["messages"] == [{"role": "user", "content": "Say 'hello'"}]
    assert captured_request["json"]["max_tokens"] == 10
    assert captured_request["timeout"] == 30


def test_401_json_parsing_when_empty(monkeypatch, capsys):
    """Test 401 error handling when response body is empty."""

    def _mock_post(*args, **kwargs):
        mock_response = MockResponse(status_code=401, text="")
        # Override json() to simulate empty/invalid JSON
        mock_response.json = MagicMock(side_effect=ValueError("No JSON object"))
        return mock_response

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("invalid-key")

    captured = capsys.readouterr()
    assert "❌ AUTHENTICATION FAILED" in captured.out


def test_prints_response_status(monkeypatch, capsys):
    """Test that response status is printed."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key")

    captured = capsys.readouterr()
    assert "Response status: 200" in captured.out
    assert "Sending test request to Mistral API..." in captured.out


# Additional regression and boundary tests


def test_validate_mistral_key_with_newlines(monkeypatch, capsys):
    """Test that API keys with newlines are handled properly."""

    def _mock_post(*args, **kwargs):
        headers = kwargs.get("headers", {})
        # Check that newlines are stripped
        assert "\n" not in headers.get("Authorization", "")
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key\n")

    captured = capsys.readouterr()
    assert "✅ SUCCESS!" in captured.out


def test_validate_mistral_key_with_tabs(monkeypatch, capsys):
    """Test that API keys with tabs are handled properly."""

    def _mock_post(*args, **kwargs):
        headers = kwargs.get("headers", {})
        # Check that tabs are stripped
        assert "\t" not in headers.get("Authorization", "")
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("\ttest-key\t")

    captured = capsys.readouterr()
    assert "✅ SUCCESS!" in captured.out


def test_validate_mistral_key_connection_error(monkeypatch, capsys):
    """Test handling of connection errors."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Failed to establish connection")

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key")

    captured = capsys.readouterr()
    assert "❌ Network error:" in captured.out
    assert "Failed to establish connection" in captured.out


def test_validate_mistral_key_ssl_error(monkeypatch, capsys):
    """Test handling of SSL errors."""

    def _mock_post(*args, **kwargs):
        raise requests.exceptions.SSLError("SSL certificate verification failed")

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key")

    captured = capsys.readouterr()
    assert "❌ Network error:" in captured.out


def test_validate_mistral_key_rate_limit_response(monkeypatch, capsys):
    """Test specific handling of 429 rate limit responses."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=429,
            text='{"error": "Rate limit exceeded"}'
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key")

    captured = capsys.readouterr()
    assert "⚠️  Unexpected response: 429" in captured.out
    assert "Rate limit exceeded" in captured.out


def test_validate_mistral_key_very_long_key(monkeypatch, capsys):
    """Boundary test: very long API key."""

    long_key = "a" * 200  # 200 character key

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "hello"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key(long_key)

    captured = capsys.readouterr()
    assert f"Length: {len(long_key)} characters" in captured.out
    assert "✅ SUCCESS!" in captured.out


def test_validate_mistral_key_response_content_extraction(monkeypatch, capsys):
    """Test that response content is correctly extracted and displayed."""

    def _mock_post(*args, **kwargs):
        return MockResponse(
            status_code=200,
            json_data={
                "choices": [
                    {
                        "message": {
                            "content": "Test response message"
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("test_api_key.requests.post", _mock_post)

    validate_mistral_key("test-key")

    captured = capsys.readouterr()
    assert "Response: Test response message" in captured.out