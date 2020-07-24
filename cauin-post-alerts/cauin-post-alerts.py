from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import telegram
import time


def get_html(url):
    driver.get(url)
    return BeautifulSoup(driver.page_source, "html.parser")


def get_element(url, css_selector):
    driver.get(url)
    BeautifulSoup(driver.page_source, "html.parser")


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
driver.get("https://cauin.cau.ac.kr/cauin/")
driver.find_element_by_name("userID").send_keys(userID)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_xpath('//*[@id="frmLogon"]/div/div/button').click()

# Get the latest title of post
while True:
    root_page = BeautifulSoup(driver.page_source, "html.parser")
    try:
        old_title = root_page.select("#aside > div > div > ul > li:nth-child(1) > a > span")[0].text
        break
    except IndexError as e:
        print(e)
        time.sleep(3)

# Scrape a new post
scrapping_period = 10
while True:
    root_page = get_html("https://cauin.cau.ac.kr/cauin/")
    for _ in range(10):
        try:
            latest_title = root_page.select("#aside > div > div > ul > li:nth-child(1) > a > span")[0].text
            break
        except IndexError as e:
            print(e)
            time.sleep(3)

    # If there is no new post, continue
    if latest_title == old_title:
        print(
            "Latest title:", latest_title, time.strftime("%c", time.localtime(time.time())),
        )
        time.sleep(scrapping_period)
        continue

    # If there is a new post
    for i in range(1, 10):
        if root_page.select("#aside > div > div > ul > li:nth-child(" + str(i) + ") > a > span")[0].text == old_title:
            break

        present_post_link = (
            "https://cauin.cau.ac.kr"
            + root_page.select("#aside > div > div > ul > li:nth-child(" + str(i) + ") > a")[0].attrs["href"]
        )
        post_page = get_html(present_post_link)
        title = post_page.select("#content > div.viewzone > div.topbox > h2")[0].text
        date = post_page.select("#content > div.viewzone > div.topbox > div.detailbox > ul > li.date > em")[0].text
        content = post_page.select("#content > div.viewzone > div.contentbox > div")[0].text

        text = "Title: " + title + "\n\n" + "Date:" + date + "\n\n" + "Content:" + content
        bot.sendMessage(chat_id=chat_id, text=text)
        print(text)

    old_title = latest_title
    time.sleep(scrapping_period)


driver.quit()

