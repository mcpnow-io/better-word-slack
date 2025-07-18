"""
Main entry point for the better_word_slack application.
Slack bot that provides translation functionality via /better command.
"""

import logging
import os

from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Slack configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


def translate_to_english(text):
    """
    Translate text to English using Google Translate API (free tier).
    You can replace this with other translation services like Azure Translator,
    AWS Translate, or DeepL API.
    """
    try:
        # Using a simple translation approach with Google Translate (unofficial)
        # For production, consider using official APIs
        import googletrans

        translator = googletrans.Translator()

        # Detect language and translate to English
        detection = translator.detect(text)
        if detection.lang == "en":
            return f"Text is already in English: {text}"

        translated = translator.translate(text, dest="en")
        return (
            f"Original ({detection.lang}): {text}\nTranslated (en): {translated.text}"
        )

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return f"Sorry, I couldn't translate that text. Error: {str(e)}"


@app.route("/slack/commands/better", methods=["POST"])
def better_command():
    """Handle the /better slash command from Slack."""

    # Verify the request is from Slack
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return "Unauthorized", 401

    # Parse the command data
    command_data = request.form
    user_id = command_data.get("user_id")
    channel_id = command_data.get("channel_id")
    text = command_data.get("text", "").strip()

    logger.info(
        f"Received /better command from user {user_id} in channel {channel_id}: {text}"
    )

    if not text:
        return jsonify(
            {
                "response_type": "ephemeral",
                "text": "Please provide text to translate. Usage: `/better 你好世界`",
            }
        )

    # Translate the text
    translation_result = translate_to_english(text)

    # Send the translation to the channel
    try:
        # Post the translation as the bot to the channel
        _ = slack_client.chat_postMessage(
            channel=channel_id,
            text=translation_result,
            username="Better Word Bot",
            icon_emoji=":globe_with_meridians:",
        )

        # Return acknowledgment to the user (ephemeral)
        return jsonify(
            {
                "response_type": "ephemeral",
                "text": "Translation sent to the channel! 🌍",
            }
        )

    except Exception as e:
        logger.error(f"Error posting to Slack: {e}")
        return jsonify(
            {
                "response_type": "ephemeral",
                "text": f"Sorry, there was an error sending the translation: {str(e)}",
            }
        )


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "better-word-slack"})


def main():
    """Main function that serves as the entry point."""
    print("better_word_slack: Improve your Slack experience, every little bit helps")

    # Check if required environment variables are set
    if not SLACK_BOT_TOKEN:
        print("Error: SLACK_BOT_TOKEN environment variable is required")
        return

    if not SLACK_SIGNING_SECRET:
        print("Error: SLACK_SIGNING_SECRET environment variable is required")
        return

    print("Starting Slack bot server...")
    print("Available endpoints:")
    print("  POST /slack/commands/better - Handle /better slash command")
    print("  GET /health - Health check")

    # Run the Flask app
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
