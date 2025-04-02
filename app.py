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
                    url = "https://8530-2601-182-c67f-96b0-a0ca-9e45-77ba-46bc.ngrok-free.app/ask"  # Flask server URL
                    params = {"query": remainder}  # Attach query as a parameter
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        out = response.json()
                        out = out['answer']
                        print(response.json())  # Parse JSON response
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

#             if text == "hello":
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text=f"Hello <@{user}>")
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")
#             elif text[0] == "!" and "generate’s mission" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text=f"Generate is a community of passionate individuals who engage in collaborative, real-world experiences to develop innovative products, the organization, its partners, and themselves.")
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")
#             elif text[0] == "!" and "generate’s values" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text="""
# Generate is under the Sherman Center, whose values must align with three core values—being developmental, inclusive, and intentional.
# In addition, Generate members are innovative, driven, empathetic, spirited, and growth-oriented.
# """)
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")
#             elif text[0] == "!" and "access isn’t working" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text="""
# If you notice a keycard reader isn’t working, please let someone know so we can diagnose the issue and quickly resolve it. A few things to try to help escalate:

# 1. **Understand if it’s an issue with your access, or with everyone’s access:**
#    - If it’s an issue with your access, please log into the Generate Ops Dashboard to check if you have been added to the access list for the spaces. This issue is common at the start of a semester.
#    - If the Dashboard says you have access, but you are experiencing an issue that no one else is, please send a message in #ops-help on Slack. Be sure to mention the space you are trying to access and what behavior you are seeing.

# 2. **If others also have the issue, and the keycard reader is not flashing red or green or making a beep when reading a card, it’s likely the reader is out of battery. In this case:**
#    - Please send a message in #ops-help on Slack.
#    - Additionally, please submit a work request here:
#      - Problem Type: Locks, Keys and Card Access
#      - Campus: Boston
#      - Building name: Hayden
#      - Floor: 0 | Basement
#      - Room number: 008 | Private Circulation Area
#      - Location within room: Front door
#      - Description: Door keycard reader requires AD400 battery change.
# """)
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")

#             elif text[0] == "!" and "ryder and cooper coming" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text="Ryder and Cooper will visit the Sherman Center on February 14, 2025, from 1:30 PM - 2:00 PM.")
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")

#             elif text[0] == "!" and "all hands" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text="All Hands is on February 20, 2025, from 7:00 PM - 9:00 PM.")
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")
            
#             elif text[0] == "!" and "showcase" in text:
#                 try:
#                     client.chat_postMessage(
#                         channel=channel, text="Showcase is on April 11, 2025, from 6:30 PM - 9:30 PM in ISEC 102.")
#                 except SlackApiError as e:
#                     print(f"Error: {e.response['error']}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    from os import getenv
    app.run(debug=True, host="0.0.0.0", port=3000)