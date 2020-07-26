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
everytime1_bot_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize constants and variables
POSTS_URL = "https://everytime.kr/375118"
BASE_URL = "https://everytime.kr"
TITLES_CSS_SELECTOR = "#container > div.wrap.articles > article > a"
DATE_CSS_SELECTOR = "#container > div.wrap.articles > article > a > div > time"
CONTENT_CSS_SELECTOR = "#container > div.wrap.articles > article > a > p"
COMMENTS_CSS_SELECTOR = ""

# Try to login
print("Login...")
driver.get("https://everytime.kr/login?redirect=/375118")
driver.find_element_by_name("userid").send_keys(USER_ID)
driver.find_element_by_name("password").send_keys(PASSWORD + "\n")

# Select the '알바.과외' category
driver.find_element_by_css_selector("#container > div.wrap.categories > div:nth-child(3) > span").click()

# Scrape the new post
scrape_posts(POSTS_URL, BASE_URL, TITLES_CSS_SELECTOR, everytime1_bot_TOKEN, get_message)

# Exit the chrome when ctrl+c pressed
driver.quit()
