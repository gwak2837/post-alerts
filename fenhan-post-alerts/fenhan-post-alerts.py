from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import telegram
import time
from queue import Queue


class SetQueue:
    def __init__(self, maxsize):
        self.items_queue = Queue(maxsize)
        self.items_set = set()

    def put(self, item):
        self.items_queue.put_nowait(item)
        self.items_set.add(item)

    def get(self):
        self.items_set.remove(self.items_queue.get_nowait())

    def have(self, item):
        return item in self.items_set

    def full(self):
        return self.items_queue.full()

    def print(self):
        print(self.items_set)


def get_elements(css_selector):
    while True:
        element = BeautifulSoup(driver.page_source, "html.parser").select(css_selector)
        if len(element) != 0:
            break
        time.sleep(1)
    return element


def get_message(title):
    driver.get(title.attrs["href"])

    date = get_elements(date_css_selector)[0].attrs["title"]

    headers = get_elements(header_css_selector)[0].contents
    header_buffer = []
    for header in headers:
        if str(type(header)) == "<class 'bs4.element.Tag'>":
            header_buffer.append(header.th.text + header.td.text)
    header = "\n".join(header_buffer)

    contents = get_elements(content_css_selector)[0].contents
    content_buffer = []
    for content in contents:
        if str(type(content)) == "<class 'bs4.element.NavigableString'>" and content != "\n":
            content_buffer.append(content.strip("\n "))
    content = "\n".join(content_buffer)

    return "题目: " + title.text.strip() + "\n\n发表于: " + date + "\n\n基本信息:\n" + header + "\n\n本文:\n" + content


def send_message(bot, message):
    for _ in range(100):
        try:
            updates = bot.getUpdates()
            break
        except telegram.error.NetworkError as e:
            print("At getUpdates():")
            print(e)
            time.sleep(1)

    chat_id_list = []
    for update in updates:
        chat_id = update.message.chat.id

        if chat_id in chat_id_list:
            continue

        for _ in range(100):
            try:
                # bot.sendMessage(chat_id=chat_id, text=message)
                break
            except telegram.error.NetworkError as e:
                print("At sendMessage():")
                print(e)
                time.sleep(1)

        chat_id_list.append(chat_id)

    print(message)


# Get ID and password from 'info.txt'
with open(".env", "r") as f:
    telegram_bot_token = f.readline()

# Connect to the telegram bot
for _ in range(100):
    try:
        fenhan_bot = telegram.Bot(token=telegram_bot_token)
        break
    except telegram.error.TimedOut as e:
        print("At Bot():")
        print(e)
        time.sleep(1)

# Setting chrome options
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("window-size=1920x1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
)
options.add_argument("lang=ko_KR")
options.add_argument("log-level=2")

# Create chrome driver
driver = webdriver.Chrome("../chromedriver", options=options)
driver.implicitly_wait(10)
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
driver.execute_script(
    "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};"
)

# Initialize constants and a variable
posts_url = "http://bbs.icnkr.com/forum.php?mod=forumdisplay&fid=1603&filter=author&orderby=dateline&sortid=344"
title_css_selector = "#separatorline ~ tbody > tr > th > a.s.xst"
date_css_selector = (
    "#postlist > div > table > tbody > tr:first-child > td:nth-child(2) > div.pi > div.pti > div.authi > em > span"
)
header_css_selector = "#postlist > div > table > tbody > tr:first-child > td:nth-child(2) > div.pct > div.pcb > div.typeoption > table > tbody"
content_css_selector = "#postlist > div > table > tbody > tr:first-child > td:nth-child(2) > div.pct > div.pcb > div.t_fsz > table > tbody > tr > td"
sent_titles = SetQueue(50)

# Get the latest title of post
print("Get the latest title of post...")
driver.get(posts_url)
old_title = get_elements(title_css_selector)[0]
send_message(fenhan_bot, get_message(old_title))
old_title_text = old_title.text.strip()
sent_titles.put(old_title_text)

# Scrape a new post
scrapping_period = 10
while True:
    driver.get(posts_url)
    titles = get_elements(title_css_selector)
    latest_title_text = titles[0].text.strip()

    # If there isn't new post, continue
    if latest_title_text == old_title_text:
        print("Latest title:", latest_title_text, time.strftime("%c", time.localtime(time.time())))
        time.sleep(scrapping_period)
        continue

    # If there is a new post
    for title in titles:
        if sent_titles.have(title.text.strip()):
            continue

        send_message(fenhan_bot, get_message(title))

        if sent_titles.full():
            sent_titles.get()

        sent_titles.put(title.text.strip())

    old_title_text = latest_title_text
    time.sleep(scrapping_period)


driver.quit()

