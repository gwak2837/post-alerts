import os
import sys
import time
import json
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class CAUinChrome(Chrome):
    def get_posts(self):
        while True:
            # Go to the community page
            if not self.go_to_page(COMMUNITY_URL):
                continue

            # Get all post links and titles in the 1st page
            post_links = self.get_bs4_elements(POST_LINKS_CSS_SELECTOR)
            post_titles = self.get_bs4_elements(POST_TITLES_CSS_SELECTOR)

            # Must get all post links and titles in the 1st page
            if post_links and post_titles:
                return [
                    (post_link["href"], post_title.get_text().strip())
                    for post_link, post_title in zip(post_links, post_titles)
                ]

    def get_message_from(self, post_link, post_title):
        for _ in range(10):
            # Go to the post details page
            if not self.go_to_page(BASE_URL + post_link):
                return "Fail to get a message with post details"

            # Handle the login alert
            try:
                self.driver.switch_to.alert.accept()
                if not self.login():
                    raise RuntimeError
            except NoAlertPresentException:
                break

        # Get the date of writing
        date = self.get_bs4_element(DATE_CSS_SELECTOR)
        date = date.get_text() if date else "None"

        # Get the post content
        content = self.get_bs4_element(CONTENT_CSS_SELECTOR)
        content = content.get_text() if content else "None"

        return "<제목> " + post_title + "\n\n<게시일> " + date + "\n\n<내용>\n" + content

    def login(self):
        print("Login...")
        if not self.go_to_page(COMMUNITY_URL):
            print("Login failed.")
            return False
        try:
            self.driver.find_element_by_name("userID").send_keys(user_id)
            self.driver.find_element_by_name("password").send_keys(password)
            self.driver.find_element_by_class_name("loginbtn").click()
            self.driver.find_element_by_id("content")  # Wait for login to complete
            return True
        except NoSuchElementException:
            print("Login failed.")
            return False


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
    while True:
        try:
            # Initialize a chrome driver for CAUin
            cauin_chrome = CAUinChrome()

            # Try to login
            cauin_chrome.login()

            # Scrape the new post
            cauin_chrome.scrape_posts(cauin_bot_token, chat_ids)

        except RuntimeError:
            cauin_chrome.driver.quit()
            time.sleep(10)
