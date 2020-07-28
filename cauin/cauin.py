import os
import sys
import time
import json
from dotenv import load_dotenv
from selenium.common.exceptions import WebDriverException

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class CAUinChrome(Chrome):
    def get_posts(self):
        # Go to the community page
        while True:
            try:
                self.driver.get(COMMUNITY_URL)
                break
            except WebDriverException as error:
                print(error, end="")
                print("    at get_posts()")
                self.login()
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

        return "<제목> " + post_title + "\n\n<게시일> " + date + "\n\n<내용>\n" + content

    def login(self):
        try:
            self.driver.get(COMMUNITY_URL)
        except WebDriverException as error:
            print(error, end="")
            print("    at login()")

        self.driver.find_element_by_name("userID").send_keys(user_id)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_class_name("loginbtn").click()
        self.driver.find_element_by_id("content")  # Wait for login to complete
        print("Login success.")


# Get user ID, password, bot token from '.env'
load_dotenv()
user_id = os.getenv("ID")
password = os.getenv("PW")
cauin_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
BASE_URL = "https://cauin.cau.ac.kr"
COMMUNITY_URL = "https://cauin.cau.ac.kr/cauin/"
POST_LINKS_CSS_SELECTOR = "#container > aside > div > div > div > ul > li > a"
POST_TITLES_CSS_SELECTOR = "#container > aside > div > div > div > ul > li > a > span"
DATE_CSS_SELECTOR = "#content > div.viewzone > div.topbox > div.detailbox > ul > li.date > em"
CONTENT_CSS_SELECTOR = "#content > div.viewzone > div.contentbox > div"
COMMENTS_CSS_SELECTOR = ""


if __name__ == "__main__":
    # Initialize a chrome driver for CAUin
    cauin_chrome = CAUinChrome(cauin_bot_token, chat_ids)

    # Try to login
    cauin_chrome.login()

    # Scrape the new post
    cauin_chrome.scrape_posts()

    # Exit the chrome when ctrl+c pressed
    cauin_chrome.driver.quit()
