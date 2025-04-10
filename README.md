# Genny - Generate Chatbot
Operations - Data Solutions - Internal Insights
Spring 2025
Chigo Ike, Matthew Li, Kaydence Lin

The purpose of the chatbot is to streamline the process of gathering organization wide information for answering internal questions in real-time.
This documentation is for internal Generate members who may implement or work on the chatbot in the future.
Knowledge of Python, APIs, LLM, Hugging Face, and Digital Ocean may be useful to understand this documentation.

## Data
The data that was used was an export of the Generate Notion Wiki (folder named "Wiki Export"). The export contained markdown files of each page. To preprocess this data, we converted all the .md into .txt files (md_to_txt.py). The text files are stored in a folder called "Wiki_txt". We cleaned the .txt files to delete any unnecessary md formatting, emojis, and empty lines and combined all the .txt files to a .json file (wiki_json.py and gen_wiki.json). 
## Slack
A Slack chatbot that can respond to messages and answer general FAQs.

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
