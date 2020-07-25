from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import bs4
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
    for _ in range(100):
        try:
            element = bs4.BeautifulSoup(driver.page_source, "html.parser").select(css_selector)
            if len(element) != 0:
                break
        except WebDriverException as e:
            print("At BeautifulSoup():", e)

        time.sleep(1)

    return element


def get_message(title):
    driver.get("https://cauin.cau.ac.kr" + title.attrs["href"])

    date = get_elements(date_css_selector)[0].text
    content = get_elements(content_css_selector)[0].text

    return "제목: " + title.text.strip() + "\n\n날짜: " + date + "\n\n내용: " + content


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
                bot.sendMessage(chat_id=chat_id, text=message)
                break
            except telegram.error.NetworkError as e:
                print("At sendMessage():")
                print(e)
                time.sleep(1)

        chat_id_list.append(chat_id)

    print("The message has sent.")


# Get ID and password from 'info.txt'
with open(".env", "r") as f:
    userID = f.readline()
    password = f.readline()
    telegram_bot_token = f.readline()

# Connect to the telegram bot
for _ in range(100):
    try:
        cauin_bot = telegram.Bot(token=telegram_bot_token)
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
posts_url = "https://cauin.cau.ac.kr/cauin/"
title_css_selector = "#container > aside > div > div > div > ul > li > a"
date_css_selector = "#content > div.viewzone > div.topbox > div.detailbox > ul > li.date > em"
content_css_selector = "#content > div.viewzone > div.contentbox > div"
sent_titles = SetQueue(15)

# Try to login
print("Login...")
driver.get(posts_url)
driver.find_element_by_name("userID").send_keys(userID)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_xpath('//*[@id="frmLogon"]/div/div/button').click()

# Get the latest title of post
print("Get the latest title of post...")
old_title = get_elements(title_css_selector)[0]
send_message(cauin_bot, get_message(old_title))
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
            break

        send_message(cauin_bot, get_message(title))

        if sent_titles.full():
            sent_titles.get()

        sent_titles.put(title.text.strip())

    old_title_text = latest_title_text
    time.sleep(scrapping_period)


driver.quit()

