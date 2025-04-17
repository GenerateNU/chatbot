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
# Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    print("Received data:", data)
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
        
    if "event" in data:
        event = data["event"]
        print(f"Event: {event}") 
        if event.get("type") == "message" and "bot_id" not in event:
            channel = event["channel"]
            user = event["user"]
            text = event["text"].lower()
        
            if text[0] == '!':
                try:
                    remainder = text[0:]
                    print(remainder)
                    url = "http://138.197.102.64:6000/ask"  # Flask server URL
                    params = {"query": remainder} 
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        out = response.json()
                        out = out['answer']
                        print(response.json())  
                    else:
                        # return print({"error": f"Request failed with status code {response.status_code}"})
                        out = {"error": f"Request failed with status code {response.status_code}"}
                    client.chat_postMessage(
                        channel=channel, text=f"{out}") # change text to the output of the model
                except SlackApiError as e:
                    print(f"Error: {e.response['error']}")
            else:
                try:
                    client.chat_postMessage(
                        channel=channel, text=f"Hello <@{user}>, please use an ! as a prefix to your question")
                except SlackApiError as e:
                    print(f"Error: {e.response['error']}")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    from os import getenv
    app.run(debug=True, host="0.0.0.0", port=3000)