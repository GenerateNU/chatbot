# Slack Chatbot

A Flask-based Slack chatbot that can respond to messages and handle various Slack events.

## Setup

1. Create a Slack App at https://api.slack.com/apps
   - Enable Socket Mode
   - Add bot token scopes: `chat:write`, `app_mentions:read`, `channels:history`, `im:history`
   - Install the app to your workspace

2. Set up your environment:
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd chatbot

   # Create and activate virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Copy example environment file and update with your Slack credentials
   cp .env.example .env
   ```

3. Update the `.env` file with your Slack credentials:
   - `SLACK_BOT_TOKEN`: Your bot's OAuth token (starts with `xoxb-`)
   - `SLACK_SIGNING_SECRET`: Your app's signing secret
   - `SLACK_APP_TOKEN`: Your app-level token (starts with `xapp-`)

## Running the Bot

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Use a tool like ngrok to expose your local server:
   ```bash
   ngrok http 5000
   ```

3. Update your Slack App's Event Subscriptions URL with the ngrok URL + `/slack/events`
   (e.g., `https://your-ngrok-url.ngrok.io/slack/events`)

## Features

- Responds to messages in channels where the bot is invited
- Basic message processing functionality
- Extensible architecture for adding more features

## Adding New Features

To add new bot responses or features:
1. Modify the `process_message()` function in `app.py`
2. Add your custom logic for handling different message types
3. Test the new functionality in your Slack workspace

## Contributing

Feel free to submit issues and enhancement requests!
