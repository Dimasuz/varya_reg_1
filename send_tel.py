import os
from pprint import pprint

import requests
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

bot_token = os.environ.get("BOT_TOKEN", "")
chat_id_g = os.environ.get("CHAT_ID_G", "")
chat_id_v = os.environ.get("CHAT_ID_V", "")
chat_id_d = os.environ.get("CHAT_ID_D", "")
message_text = "Привет!"


def send_telegram(message_text, chat_id=chat_id_g):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message_text,
    }

    try:
        response = requests.get(url, params=params)
    except:
        print("Error send massage to Telegram.")

    if response.status_code == 200:
        json_data = response.json()
        # pprint(json_data)
        message = "Send to Telegram is OK."
        print(message)
        return message
    else:
        message = f"Send to Telegram is ERROR: {response.status_code}"
        print(message)
        return message


def test():
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    pprint(requests.get(url).json())


if __name__ == "__main__":
    send_telegram(message_text)
    test()
