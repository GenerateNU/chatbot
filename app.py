from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set bot token (from .env file)
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Check if the token is loaded correctly
if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN is missing. Check your .env file.")

client = WebClient(token=SLACK_BOT_TOKEN)

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

if __name__ == "__main__":
    app.run(port=3000)
