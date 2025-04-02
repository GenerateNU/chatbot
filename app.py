from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set bot token (from .env file)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# NOTION_KEY = os.getenv("NOTION_KEY")
# NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

# Check if the token is loaded correctly
# if not SLACK_BOT_TOKEN or not NOTION_KEY or not NOTION_PAGE_ID:
#     raise ValueError("Missing one or more required environment variables.")

# Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

# Notion API
# NOTION_HEADERS = {
#     "Authorization": f"Bearer {NOTION_KEY}",
#     "Content-Type": "application/json",
#     "Notion-Version": "2022-06-28"
# }

@app.route("/")
def hello_world():
    return "Slack Chatbot is running!"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    
    # Verify Slack URL challenge
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})
    
    # Handle message events
    if data.get("event", {}).get("type") == "message":
        try:
            event = data["event"]
            channel = event.get("channel")
            text = event.get("text")
            
            # Don't respond to bot's own messages
            if event.get("bot_id"):
                return jsonify({"status": "ignored bot message"})
            
            # Process the message and send response
            response = process_message(text)
            
            # Send response back to Slack
            client.chat_postMessage(
                channel=channel,
                text=response
            )
            
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
    
    return jsonify({"status": "ok"})

def process_message(text):
    # Add your chatbot logic here
    return f"You said: {text}"

# def scrape_notion(input):
#     notion_url = f"https://api.notion.com/v1/databases/{NOTION_PAGE_ID}/query"
#
#     # Fetch all pages
#     response = requests.post(notion_url, headers=NOTION_HEADERS)
#     if response.status_code != 200:
#         return "Error fetching data from Notion."
#
#     pages = response.json().get("results", [])
#
#     # Extract content and search
#     for page in pages:
#         properties = page.get("properties", {})
#         name = properties.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Untitled")
#         content = properties.get("Content", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
#
#         if input.lower() in content.lower():
#             return f"*Found in Notion:* {name}\n{content}"
#
#     return "No relevant data found in Notion."

if __name__ == "__main__":
    from os import getenv
    app.run(debug=True, host="0.0.0.0", port=3000)
