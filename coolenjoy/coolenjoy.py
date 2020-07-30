import os
import sys
import time
import json
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class CoolenjoyChrome(Chrome):
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
        # Go to the post details page
        if not self.go_to_page(post_link):
            return "Fail to get a message with post details"

        # Get the date of writing
        date_element = self.get_bs4_element(DATE_CSS_SELECTOR)
        date = date_element.get_text() if date_element else "None"

        # Get the post content
        content_element = self.get_bs4_element(CONTENT_CSS_SELECTOR)
        content = content_element.get_text() if content_element else "None"

        # Get the link of the product
        links_element = self.get_bs4_elements(LINKS_CSS_SELECTOR)
        links_buffer = [link_element["href"] for link_element in links_element]
        links = "\n".join(links_buffer)

        return "<제목> " + post_title + "\n\n<게시일> " + date + "\n\n<내용>\n" + content + "\n\n<제품 링크>\n" + links

    def login(self):
        print("Login...")
        if not self.go_to_page(COMMUNITY_URL):
            print("Login failed.")
            return False
        try:
            self.driver.find_element_by_name("mb_id").send_keys(user_id)
            self.driver.find_element_by_name("mb_password").send_keys(password + "\n")
            self.driver.find_element_by_id("fboardlist")  # Wait for login to complete
            return True
        except NoSuchElementException:
            print("Login failed.")
            return False


# Get user ID, password, bot token from '.env'
load_dotenv()
user_id = os.getenv("ID")
password = os.getenv("PW")
coolenjoy1_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
COMMUNITY_URL = "http://www.coolenjoy.net/bbs/jirum"
"#fboardlist > div > table > tbody > tr:nth-child(3)"
POST_LINKS_CSS_SELECTOR = "#fboardlist > div > table > tbody > tr:not(.bo_notice) > td.td_subject > a"
POST_TITLES_CSS_SELECTOR = "#fboardlist > div > table > tbody > tr:not(.bo_notice) > td.td_subject > a"
DATE_CSS_SELECTOR = "#bo_v_info > strong:nth-child(4)"
CONTENT_CSS_SELECTOR = "#bo_v_con"
LINKS_CSS_SELECTOR = "#bo_v_link > ul > li > a"
COMMENTS_CSS_SELECTOR = ""


if __name__ == "__main__":
    # Initialize a chrome driver for CAUin
    coolenjoy_chrome = CoolenjoyChrome()

    """
    # Try to login
    coolenjoy_chrome.login()
    """

    # Scrape the new post
    coolenjoy_chrome.scrape_posts(coolenjoy1_bot_token, chat_ids)

    # Exit the chrome when ctrl+c pressed
    coolenjoy_chrome.driver.quit()
