import os
import sys
from dotenv import load_dotenv

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import driver
from common.functions import get_elements
from common.functions import scrape_posts


# - driver.page_source
def get_message(title):
    date = get_elements(DATE_CSS_SELECTOR)[0].text
    content = get_elements(CONTENT_CSS_SELECTOR)[0].text

    return "제목: " + title + "\n\n날짜: " + date + "\n\n내용: " + content


# Get user ID, password, bot token from '.env'
load_dotenv()
USER_ID = os.getenv("ID")
PASSWORD = os.getenv("PW")
cauin_bot_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Initialize constants and variables
POSTS_URL = "https://cauin.cau.ac.kr/cauin/"
BASE_URL = "https://cauin.cau.ac.kr"
TITLES_CSS_SELECTOR = "#container > aside > div > div > div > ul > li > a"
DATE_CSS_SELECTOR = "#content > div.viewzone > div.topbox > div.detailbox > ul > li.date > em"
CONTENT_CSS_SELECTOR = "#content > div.viewzone > div.contentbox > div"

# Try to login
print("Login...")
driver.get(POSTS_URL)
driver.find_element_by_name("userID").send_keys(USER_ID)
driver.find_element_by_name("password").send_keys(PASSWORD)
driver.find_element_by_xpath('//*[@id="frmLogon"]/div/div/button').click()

# Scrape the new post
scrape_posts(POSTS_URL, BASE_URL, TITLES_CSS_SELECTOR, cauin_bot_TOKEN, get_message)

# Exit the chrome when ctrl+c pressed
driver.quit()
