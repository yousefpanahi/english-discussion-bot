import os
import requests
from datetime import datetime, timezone

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


# Get current UTC time
now = datetime.now(timezone.utc)

day = now.strftime("%A")
hour = now.hour
minute = now.minute

# Session days
session_days = ["Saturday", "Monday", "Wednesday"]


# 1. Class reminder — 13:30 UTC
if day in session_days and hour == 13 and minute < 30:

    message = """Hello Everyone. Kindly Reminder

We will have the English Free Discussion meeting today at 4:30 PM - 5:30 PM (UTC)."""

    send_message(message)


# 2. Join class — 16:30 UTC
elif day in session_days and hour == 16 and minute < 30:

    message = """Everybody please join Class.

Meeting Link:
https://meet.google.com/vtg-anvk-vgn"""

    send_message(message)
