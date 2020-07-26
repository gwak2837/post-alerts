import time
import queue
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import bs4
import telegram


class SetQueue:
    def __init__(self, maxsize):
        self.items_queue = queue.Queue(maxsize)
        self.items_set = set()

    # if queue is full, pop the oldest item and put the new item
    def put(self, item):
        if self.items_queue.full():
            self.items_set.remove(self.items_queue.get_nowait())
        self.items_queue.put_nowait(item)
        self.items_set.add(item)

    def have(self, item):
        return item in self.items_set

    def print(self):
        print(self.items_set)


# Connect to the telegram bot
# - pure function
def get_telegram_bot(token):
    for _ in range(100):
        try:
            telegram_bot = telegram.Bot(token=token)
            break
        except telegram.error.TimedOut as error:
            print("At telegram.Bot():", error)
            time.sleep(1)

    for _ in range(100):
        try:
            updates = telegram_bot.get_updates(timeout=10)
            break
        except telegram.error.NetworkError as error:
            print("At telegram_bot.get_updates():", error)
            time.sleep(1)

    chat_id_set = set()
    for update in updates:
        chat_id_set.add(update.message.chat.id)

    return telegram_bot, chat_id_set


# Send the message to the telegram bot
# - pure function
def send_message(telegram_bot, chat_ids, message):
    message_sent = False

    for chat_id in chat_ids:
        for _ in range(100):
            try:
                telegram_bot.send_message(chat_id=chat_id, text=message)
                message_sent = True
                break
            except telegram.error.NetworkError as error:
                print("At telegram_bot.send_message():", error)
                time.sleep(1)

    if message_sent:
        print("The message has sent.", message[: message.find("\n")], "...")
    else:
        print("Failed to send message because there is no recipient")

    return message_sent


# - driver.page_source
def get_elements(css_selector, wait_sec=100):
    for _ in range(wait_sec):
        try:
            element = bs4.BeautifulSoup(driver.page_source, "html.parser").select(css_selector)
            if len(element) != 0:
                break
        except WebDriverException as error:
            print("At bs4.BeautifulSoup():", error)

        time.sleep(1)

    return element


# 이 함수를 실행하기 전에 글 목록이 있는 페이지로 이동한다. (필요 시 로그인해야 함)
# - driver.get()
def scrape_posts(posts_url, base_url, titles_css_selector, token, get_message, period=10, queue_size=0):
    try:
        print("Connect to the telegram bot...")
        telegram_bot, chat_id_set = get_telegram_bot(token)

        print("Get the latest title of post...")
        titles = get_elements(titles_css_selector)
        sent_titles = SetQueue(len(titles) if queue_size == 0 else queue_size)
        old_title = titles[0].text.strip()
        driver.get(base_url + titles[0].attrs["href"])
        if not send_message(telegram_bot, chat_id_set, get_message(old_title)):
            return

        sent_titles.put(old_title)

        # Scrape a new post
        while True:
            driver.get(posts_url)
            titles = get_elements(titles_css_selector)
            latest_title = titles[0].text.strip()

            # If there isn't new post, continue
            if latest_title == old_title:
                print("Latest title:", latest_title, time.strftime("%c", time.localtime(time.time())))
                time.sleep(period)
                continue

            # If there is a new post
            for title in titles:
                title_text = title.text.strip()
                if sent_titles.have(title_text):
                    break

                driver.get(base_url + title.attrs["href"])
                if send_message(telegram_bot, chat_id_set, get_message(title_text)):
                    sent_titles.put(title_text)

            old_title = latest_title
            time.sleep(period)

    except KeyboardInterrupt:
        print("Bye")


# Setting chrome options
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
# options.add_argument("no-sandbox")
options.add_argument("disable-dev-shm-usage")
options.add_argument("window-size=1920x1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
)
options.add_argument("lang=ko_KR")
options.add_argument("log-level=2")
prefs = {
    "profile.default_content_setting_values": {
        "cookies": 1,
        "images": 2,
        "plugins": 2,
        "popups": 2,
        "geolocation": 2,
        "notifications": 2,
        "auto_select_certificate": 2,
        "fullscreen": 2,
        "mouselock": 2,
        "mixed_script": 2,
        "media_stream": 2,
        "media_stream_mic": 2,
        "media_stream_camera": 2,
        "protocol_handlers": 2,
        "ppapi_broker": 2,
        "automatic_downloads": 2,
        "midi_sysex": 2,
        "push_messaging": 2,
        "ssl_cert_decisions": 2,
        "metro_switch_to_desktop": 2,
        "protected_media_identifier": 2,
        "app_banner": 2,
        "site_engagement": 2,
        "durable_storage": 2,
    }
}
options.add_experimental_option("prefs", prefs)

# Create chrome driver
driver = webdriver.Chrome("../chromedriver", options=options)
driver.implicitly_wait(10)
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
driver.execute_script(
    "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};"
)
