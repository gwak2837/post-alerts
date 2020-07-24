from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import telegram
import time


def get_html(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")


# Get ID and password from 'info.txt'
with open(".env", "r") as f:
    userID = f.readline()
    password = f.readline()
    telegram_bot_token = f.readline()

# Connect to the telegram bot
bot = telegram.Bot(token=telegram_bot_token)
chat_id = bot.getUpdates()[-1].message.chat.id

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


# Try to login
print("Login...")
driver.get("http://www.coolenjoy.net/bbs/jirum")
driver.find_element_by_name("mb_id").send_keys(userID)
driver.find_element_by_name("mb_password").send_keys(password)

# Get the latest title of post
print("Get the latest title of post...")
latest_title_css_selector = "#fboardlist > div > table > tbody > tr:nth-child(3) > td.td_subject > a"
while True:
    root_page = BeautifulSoup(driver.page_source, "html.parser")
    try:
        old_title = root_page.select(latest_title_css_selector)[0].text.strip()
        break
    except IndexError as e:
        print(e)
        time.sleep(3)

# Scrape a new post
scrapping_period = 10
while True:
    root_page = get_html("http://www.coolenjoy.net/bbs/jirum")
    latest_title = root_page.select(latest_title_css_selector)[0].text.strip()

    # If there is no new post, continue
    if latest_title == old_title:
        print("Latest title:", latest_title, time.strftime("%c", time.localtime(time.time())))
        time.sleep(scrapping_period)
        continue

    # If there is a new post
    for i in range(3, 5):
        ith_title = root_page.select(
            "#fboardlist > div > table > tbody > tr:nth-child(" + str(i) + ") > td.td_subject > a"
        )[0].text.strip()
        if ith_title == old_title:
            break

        present_post_link = root_page.select(
            "#fboardlist > div > table > tbody > tr:nth-child(" + str(i) + ") > td.td_subject > a"
        )[0].attrs["href"]
        post_page = get_html(present_post_link)
        title = post_page.select("#bo_v_title")[0].text.strip()
        date = post_page.select("#bo_v_info > strong:nth-child(4)")[0].text
        content = post_page.select("#bo_v_con")[0].text.strip()

        text = "Title: " + title + "\n\n" + "Date:" + date + "\n\n" + "Content:" + content
        for _ in range(10):
            try:
                bot.sendMessage(chat_id=chat_id, text=text)
                break
            except telegram.error.NetworkError as e:
                print(e)
                time.sleep(3)
        print(text)

    old_title = latest_title
    time.sleep(scrapping_period)


driver.quit()

