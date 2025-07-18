# better_word_slack
Improve your Slack experience, every little bit helps

A Slack bot that provides text translation functionality via the `/better` slash command. When users type `/better <text>` in Slack, the bot translates the text to English and posts it to the channel.

## Features

- 🌍 **Automatic Translation**: Translates any text to English
- 🤖 **Slack Integration**: Works seamlessly with Slack's slash commands
- 🚀 **Easy Setup**: Simple configuration with environment variables
- 📱 **Channel Posting**: Translated text is posted directly to the channel

## How to Use

In any Slack channel where the bot is installed, simply type:
```
/better 你好世界
```

The bot will:
1. Detect the language of your text
2. Translate it to English
3. Post the translation to the channel

## Setup Instructions

### 1. Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Enter app name (e.g., "Better Word Bot") and select your workspace
4. Click "Create App"

### 2. Configure Bot Permissions

1. In your app settings, go to "OAuth & Permissions"
2. Under "Scopes" → "Bot Token Scopes", add these permissions:
   - `chat:write` - To post messages to channels
   - `commands` - To receive slash commands

### 3. Create Slash Command

1. Go to "Slash Commands" in your app settings
2. Click "Create New Command"
3. Configure:
   - **Command**: `/better`
   - **Request URL**: `https://yourdomain.com/slack/commands/better`
   - **Short Description**: `Translate text to English`
   - **Usage Hint**: `text to translate`

### 4. Install App to Workspace

1. Go to "Install App" in your app settings
2. Click "Install to Workspace"
3. Authorize the app

### 5. Get Your Tokens

1. **Bot User OAuth Token**: Found in "OAuth & Permissions" (starts with `xoxb-`)
2. **Signing Secret**: Found in "Basic Information" → "App Credentials"

### 6. Set Up Your Environment

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual tokens:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_SIGNING_SECRET=your-actual-signing-secret
   PORT=3000
   ```

## Development

### Local Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install
```

### Running Locally

```bash
# Load environment variables
source .env

# Run the bot
python run.py
```

For local development with Slack, you'll need to expose your local server to the internet using a tool like [ngrok](https://ngrok.com/):

```bash
# In another terminal
ngrok http 3000

# Use the HTTPS URL (e.g., https://abc123.ngrok.io) as your Request URL in Slack
```

## API Endpoints

- `POST /slack/commands/better` - Handles the `/better` slash command
- `GET /health` - Health check endpoint

## Translation Service

The bot currently uses the `googletrans` library for translation. For production use, consider using official translation APIs:

- **Google Cloud Translation API**
- **Azure Translator Text API**
- **AWS Translate**
- **DeepL API**

## Troubleshooting

### Common Issues

1. **"Unauthorized" error**: Check your `SLACK_SIGNING_SECRET`
2. **Bot not responding**: Verify your `SLACK_BOT_TOKEN` and bot permissions
3. **Command not found**: Make sure the slash command is properly configured in Slack
4. **Translation errors**: Check internet connectivity and translation service availability

### Logs

The application logs important events. Check your deployment logs if something isn't working.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.