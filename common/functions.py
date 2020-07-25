import telegram
import time


def send_message(bot, message):
    for _ in range(100):
        try:
            updates = bot.getUpdates()
            break
        except telegram.error.NetworkError as e:
            print("At getUpdates():", e)
            time.sleep(1)

    chat_id_list = []
    for update in updates:
        chat_id = update.message.chat.id

        if chat_id in chat_id_list:
            continue

        for _ in range(100):
            try:
                bot.sendMessage(chat_id=chat_id, text=message)
                break
            except telegram.error.NetworkError as e:
                print("At sendMessage():", e)
                time.sleep(1)

        chat_id_list.append(chat_id)

    print("The message has sent.")
