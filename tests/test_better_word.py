"""
Tests for the better_word_slack application.
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from better_word import app, translate_to_english  # noqa: E402


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert data["service"] == "better-word-slack"


@patch("better_word.signature_verifier.is_valid_request")
@patch("better_word.slack_client.chat_postMessage")
def test_better_command_success(mock_post_message, mock_verify, client):
    """Test successful /better command handling."""
    # Mock verification to pass
    mock_verify.return_value = True

    # Mock Slack API response
    mock_post_message.return_value = {"ok": True}

    # Mock form data
    form_data = {"user_id": "U123456", "channel_id": "C123456", "text": "你好"}

    with patch("better_word.translate_to_english") as mock_translate:
        mock_translate.return_value = "Original (zh): 你好\nTranslated (en): Hello"

        response = client.post("/slack/commands/better", data=form_data)
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["response_type"] == "ephemeral"
        assert "Translation sent" in data["text"]


@patch("better_word.signature_verifier.is_valid_request")
def test_better_command_no_text(mock_verify, client):
    """Test /better command with no text."""
    mock_verify.return_value = True

    form_data = {"user_id": "U123456", "channel_id": "C123456", "text": ""}

    response = client.post("/slack/commands/better", data=form_data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data["response_type"] == "ephemeral"
    assert "Please provide text" in data["text"]


def test_better_command_unauthorized(client):
    """Test /better command with invalid signature."""
    form_data = {"user_id": "U123456", "channel_id": "C123456", "text": "hello"}

    response = client.post("/slack/commands/better", data=form_data)
    assert response.status_code == 401


@patch("googletrans.Translator")
def test_translate_to_english(mock_translator_class):
    """Test translation functionality."""
    # Mock translator instance
    mock_translator = MagicMock()
    mock_translator_class.return_value = mock_translator

    # Mock detection
    mock_detection = MagicMock()
    mock_detection.lang = "zh"
    mock_translator.detect.return_value = mock_detection

    # Mock translation
    mock_translation = MagicMock()
    mock_translation.text = "Hello"
    mock_translator.translate.return_value = mock_translation

    result = translate_to_english("你好")

    assert "Original (zh): 你好" in result
    assert "Translated (en): Hello" in result


@patch("googletrans.Translator")
def test_translate_already_english(mock_translator_class):
    """Test translation of English text."""
    # Mock translator instance
    mock_translator = MagicMock()
    mock_translator_class.return_value = mock_translator

    # Mock detection for English
    mock_detection = MagicMock()
    mock_detection.lang = "en"
    mock_translator.detect.return_value = mock_detection

    result = translate_to_english("Hello")

    assert "Text is already in English" in result
    assert "Hello" in result


if __name__ == "__main__":
    pytest.main([__file__])
