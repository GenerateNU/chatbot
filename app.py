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
NOTION_KEY = os.getenv("NOTION_KEY")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

# Check if the token is loaded correctly
if not SLACK_BOT_TOKEN or not NOTION_KEY or not NOTION_PAGE_ID:
    raise ValueError("Missing one or more required environment variables.")

# Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

# Notion API
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    if "event" in data:
        event = data["event"]
        if event.get("type") == "message" and "bot_id" not in event:
            channel = event["channel"]
            user = event["user"]
            text = event["text"]

            if text.lower() == "hello":
                try:
                    client.chat_postMessage(
                        channel=channel, text=f"Hello <@{user}>")
                except SlackApiError as e:
                    print(f"Error: {e.response['error']}")

    return jsonify({"status": "ok"}), 200


def scrape_notion(input):
    notion_url = f"https://api.notion.com/v1/databases/{NOTION_PAGE_ID}/query"

    # Fetch all pages
    response = requests.post(notion_url, headers=NOTION_HEADERS)
    if response.status_code != 200:
        return "Error fetching data from Notion."

    pages = response.json().get("results", [])

    # Extract content and search
    for page in pages:
        properties = page.get("properties", {})
        name = properties.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Untitled")
        content = properties.get("Content", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")

        if input.lower() in content.lower():
            return f"📌 *Found in Notion:* {name}\n{content}"

    return "No relevant data found in Notion."

if __name__ == "__main__":
    app.run(port=3000)
