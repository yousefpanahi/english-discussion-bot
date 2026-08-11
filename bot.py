import os
import requests
import sys

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print(response.json())


# The workflow tells us which message to send
message_type = os.environ.get("MESSAGE_TYPE")


# ---------------------------------------
# 1. CLASS REMINDER
# ---------------------------------------

if message_type == "reminder":

    message = """Hello Everyone. Kindly Reminder

We will have the English Free Discussion meeting today at 4:30 PM - 5:30 PM (UTC)."""

    send_message(message)


# ---------------------------------------
# 2. JOIN CLASS
# ---------------------------------------

elif message_type == "join":

    message = """Everybody please join Class.

Meeting Link:
https://meet.google.com/vtg-anvk-vgn"""

    send_message(message)


else:

    print("No valid MESSAGE_TYPE was provided.")
    sys.exit(1)
