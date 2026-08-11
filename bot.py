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


# Current UTC date and time
now = datetime.now(timezone.utc)

day = now.strftime("%A")
hour = now.hour
minute = now.minute

# Our discussion days
session_days = ["Saturday", "Monday", "Wednesday"]


# ---------------------------------------------------
# 1. CLASS REMINDER — 13:30 UTC
# ---------------------------------------------------

if day in session_days and hour == 13 and 25 <= minute <= 45:

    message = """Hello Everyone. Kindly Reminder

We will have the English Free Discussion meeting today at 4:30 PM - 5:30 PM (UTC)."""

    send_message(message)


# ---------------------------------------------------
# 2. JOIN CLASS — 16:30 UTC
# ---------------------------------------------------

elif day in session_days and hour == 16 and 25 <= minute <= 45:

    message = """Everybody please join Class.

Meeting Link:
https://meet.google.com/vtg-anvk-vgn"""

    send_message(message)
