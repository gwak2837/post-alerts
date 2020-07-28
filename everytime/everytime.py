import os
import sys
import time
import json
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException


# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class EverytimeChrome(Chrome):
    def get_posts(self):
        # Go to the community page and select the '알바.과외' category
        while True:
            try:
                self.driver.get(COMMUNITY_URL)
                self.driver.find_element_by_css_selector(CATEGORY_CSS_SELECTOR).click()
                break
            except (WebDriverException, NoSuchElementException) as error:
                print(error, end="")
                print("    at get_posts()")
                time.sleep(10)

        # Get all post links and titles
        post_links = self.must_get_bs4_elements(POST_LINKS_CSS_SELECTOR)
        post_titles = self.must_get_bs4_elements(POST_TITLES_CSS_SELECTOR)

        return [(post_link["href"], post_title.text.strip()) for post_link, post_title in zip(post_links, post_titles)]

    def get_message_from(self, post_link, post_title):
        # Go to the post details page
        try:
            self.driver.get(BASE_URL + post_link)
        except WebDriverException as error:
            print(error, end="")
            print("    at get_message_from()")
            return error

        # Get the date of writing
        date = self.get_bs4_element(DATE_CSS_SELECTOR)
        date = date.string if date else "None"

        # Get the post content
        content = self.get_bs4_element(CONTENT_CSS_SELECTOR)
        content = content.get_text() if content else "None"

        return "<제목> " + post_title + "\n\n<게시일> " + date + "\n\n<내용>\n" + content

    def login(self):
        # Try to login
        try:
            self.driver.get(LOGIN_URL)
        except WebDriverException as error:
            print(error, end="")
            print("    at login()")

        everytime_chrome.driver.find_element_by_name("userid").send_keys(user_id)
        everytime_chrome.driver.find_element_by_name("password").send_keys(password + "\n")
        everytime_chrome.driver.find_element_by_id("writeArticleButton")  # Wait for login to complete
        print("Login success.")


# Get user ID, password, bot token from '.env'
load_dotenv()
user_id = os.getenv("ID")
password = os.getenv("PW")
everytime1_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
BASE_URL = "https://everytime.kr"
COMMUNITY_URL = "https://everytime.kr/375118"
LOGIN_URL = "https://everytime.kr/login?redirect=/375118"
CATEGORY_CSS_SELECTOR = "#container > div.wrap.categories > div:nth-child(3) > span"
POST_LINKS_CSS_SELECTOR = "#container > div.wrap.articles > article > a"
POST_TITLES_CSS_SELECTOR = "#container > div.wrap.articles > article > a > h2"
DATE_CSS_SELECTOR = "#container > div.wrap.articles > article > a > div > time"
CONTENT_CSS_SELECTOR = "#container > div.wrap.articles > article > a > p"
COMMENTS_CSS_SELECTOR = ""

if __name__ == "__main__":
    # Initialize a chrome driver for Everytie
    everytime_chrome = EverytimeChrome(everytime1_bot_token, chat_ids)

    # Try to login
    everytime_chrome.login()

    # Scrape the new post after logging in
    everytime_chrome.scrape_posts()

    # Exit the chrome when ctrl+c pressed
    everytime_chrome.driver.quit()
