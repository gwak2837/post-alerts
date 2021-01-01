import os
import sys
import time
import json
import datetime
import requests
import telegram
from dotenv import load_dotenv

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import TelegramBot


load_dotenv()
apple_pickup_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

print("Connect to the telegram bot...")
telegram_bot = TelegramBot(apple_pickup_bot_token, chat_ids)
telegram_bot.send_message("hello first message")

URL = "https://www.apple.com/kr-k12/shop/retail/pickup-message?pl=true&parts.0=MYFP2KH/A&location=06982"

print("Fetching availability of picking iPad air 4 up...")
while True:
    try:
        response = requests.get(URL)
    except Exception as e:
        print(e)

    air4 = response.json()["body"]["stores"][0]["partsAvailability"]["MYFP2KH/A"]
    message = f'{air4["storePickupQuote"]}, {air4["storePickupProductTitle"]}, {datetime.datetime.now()}'

    if air4["storeSelectionEnabled"]:
        telegram_bot.send_message(message)
        time.sleep(3600)
    else:
        print(message)

    time.sleep(10)
