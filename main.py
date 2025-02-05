from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Replace with your bot token
SLACK_BOT_TOKEN = "xoxb-8401469809890-8424426773904-wsq9PmLqkHTO1UuSz44ZIQVK"

client = WebClient(token=SLACK_BOT_TOKEN)

try:
    response = client.chat_postMessage(
        channel="#general", text="Hello, Slack!")
    print("Message sent:", response["ts"])
except SlackApiError as e:
    print(f"Error sending message: {e.response['error']}")
