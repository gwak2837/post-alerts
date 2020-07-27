import os
import sys
import time
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
                print(error)
                time.sleep(10)

        # Get all post links and titles
        post_links = self.must_get_bs4_elements(POST_LINKS_CSS_SELECTOR)
        post_titles = self.must_get_bs4_elements(POST_TITLES_CSS_SELECTOR)

        return [
            (post_link.attrs["href"], post_title.text.strip()) for post_link, post_title in zip(post_links, post_titles)
        ]

    def get_message_from(self, post_link, post_title):
        # Go to the post details page
        self.driver.get(BASE_URL + post_link)

        # Get the date of writing and the post content
        date = self.get_bs4_element(DATE_CSS_SELECTOR).get_text()
        content = self.get_bs4_element(CONTENT_CSS_SELECTOR).get_text()

        return "제목: " + post_title + "\n\n날짜: " + date + "\n\n내용:\n" + content


# Get user ID, password, bot token from '.env'
load_dotenv()
user_id = os.getenv("ID")
password = os.getenv("PW")
cauin_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize constants and variables
cauin_chrome = CAUinChrome(cauin_bot_token)
POST_LINKS_CSS_SELECTOR = "#container > aside > div > div > div > ul > li > a"
POST_TITLES_CSS_SELECTOR = "#container > aside > div > div > div > ul > li > a > span"
DATE_CSS_SELECTOR = "#content > div.viewzone > div.topbox > div.detailbox > ul > li.date > em"
CONTENT_CSS_SELECTOR = "#content > div.viewzone > div.contentbox > div"
COMMENTS_CSS_SELECTOR = ""
COMMUNITY_URL = "https://cauin.cau.ac.kr/cauin/"
BASE_URL = "https://cauin.cau.ac.kr"

# Try to login
cauin_chrome.driver.get(COMMUNITY_URL)
cauin_chrome.driver.find_element_by_name("userID").send_keys(user_id)
cauin_chrome.driver.find_element_by_name("password").send_keys(password)
cauin_chrome.driver.find_element_by_class_name("loginbtn").click()
cauin_chrome.driver.find_element_by_id("content")  # Wait for login to complete
print("Login success.")

# Scrape the new post
cauin_chrome.scrape_posts()

# Exit the chrome when ctrl+c pressed
cauin_chrome.driver.quit()

