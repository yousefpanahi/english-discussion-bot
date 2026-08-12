import os
import sys
import json
import requests


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Your BBC content channel
BBC_CHANNEL_ID = "-1003760493970"

# First BBC episode starts at message 2
FIRST_EPISODE_MESSAGE_ID = 2

# File that remembers which episode was last sent
COUNTER_FILE = "episode_counter.txt"


# ==================================================
# SEND TELEGRAM MESSAGE
# ==================================================

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

    if not response.ok:
        raise Exception("Failed to send message")


# ==================================================
# COPY TELEGRAM MESSAGE
# ==================================================

def copy_message(message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/copyMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "from_chat_id": BBC_CHANNEL_ID,
            "message_id": message_id
        }
    )

    print(response.json())

    if not response.ok:
        raise Exception(f"Failed to copy message {message_id}")


# ==================================================
# GET CURRENT EPISODE NUMBER
# ==================================================

def get_episode_number():
    if not os.path.exists(COUNTER_FILE):
        return 0

    with open(COUNTER_FILE, "r") as file:
        return int(file.read().strip())


# ==================================================
# SAVE EPISODE NUMBER
# ==================================================

def save_episode_number(number):
    with open(COUNTER_FILE, "w") as file:
        file.write(str(number))


# ==================================================
# GET QUESTIONS FOR EPISODE
# ==================================================

def get_questions(episode_number):
    filename = f"questions/episode{episode_number:03d}.json"

    if not os.path.exists(filename):
        raise Exception(f"Questions file not found: {filename}")

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


# ==================================================
# MESSAGE TYPE
# ==================================================

message_type = os.environ.get("MESSAGE_TYPE")


# ==================================================
# 1. CLASS REMINDER
# ==================================================

if message_type == "reminder":

    message = """Hello Everyone. Kindly Reminder

We will have the English Free Discussion meeting today at 4:30 PM - 5:30 PM (UTC)."""

    send_message(message)


# ==================================================
# 2. JOIN CLASS
# ==================================================

elif message_type == "join":

    message = """Everybody please join Class.

Meeting Link:
https://meet.google.com/vtg-anvk-vgn"""

    send_message(message)


# ==================================================
# 3. BBC 6 MINUTE ENGLISH EPISODE
# ==================================================

elif message_type == "bbc":

    # Get the last episode that was sent
    episode_number = get_episode_number()

    # The next episode
    next_episode = episode_number + 1

    # Calculate the first BBC message ID
    first_message_id = (
        FIRST_EPISODE_MESSAGE_ID
        + (episode_number * 3)
    )

    print(f"Sending Episode {next_episode}")

    print(
        f"Message IDs: {first_message_id}, "
        f"{first_message_id + 1}, "
        f"{first_message_id + 2}"
    )

    # Load questions for this episode
    episode_data = get_questions(next_episode)

    title = episode_data["title"]
    questions = episode_data["questions"]

    # Send introduction first
    message = """Hello Guys

The next topic for our free discussion will be the episode below."""

    send_message(message)

    # Copy the three BBC messages
    copy_message(first_message_id)
    copy_message(first_message_id + 1)
    copy_message(first_message_id + 2)

    # Discussion introduction
    discussion_message = f"""📚 Discussion Time!

Today's Topic: {title}

Please discuss the following questions and try to speak as much as possible.

Remember:
• There are no perfect answers.
• Respect different opinions.
• Help others practice English.

Good luck and enjoy the discussion! 😊"""

    send_message(discussion_message)

    # Send the six questions
    questions_message = "💬 Discussion Questions\n\n"

    for i, question in enumerate(questions, start=1):
        questions_message += f"{i}️⃣ {question}\n\n"

    send_message(questions_message)

    # Only move to the next episode after everything worked
    save_episode_number(next_episode)

    print(f"Episode {next_episode} completed successfully.")


# ==================================================
# INVALID MESSAGE TYPE
# ==================================================

else:

    print("No valid MESSAGE_TYPE was provided.")
    sys.exit(1)
