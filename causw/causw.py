import os
import sys
import time
import json
from dotenv import load_dotenv

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class CAUSWChrome(Chrome):
    def get_posts(self):
        while True:
            # Go to the community page
            if not self.go_to_page(COMMUNITY_URL):
                continue

            # Get all post links and titles in the 1st page
            post_links = self.get_bs4_elements(POST_LINKS_CSS_SELECTOR)
            post_titles = self.get_bs4_elements(POST_TITLES_CSS_SELECTOR)
            post_states = self.get_bs4_elements(POST_STATES_CSS_SELECTOR)

            # Must get all post links and titles in the 1st page
            if post_links and post_titles:
                a = [
                    (post_link["href"][1:], post_title.get_text().strip() + post_state.get_text().strip())
                    for post_link, post_title, post_state in zip(post_links, post_titles, post_states)
                ]
                print(a)
                time.sleep(1000)
                return a

    def get_message_from(self, post_link, post_title):
        # Go to the post details page
        if not self.go_to_page(post_link):
            return "Fail to get a message with post details"

        # Get the date of writing
        date = self.get_bs4_element(DATE_CSS_SELECTOR)
        date = date["title"] if date else "None"

        # Get the summary of the post
        # header_ths = self.get_bs4_elements(HEADER_TH_CSS_SELECTOR)
        # header_tds = self.get_bs4_elements(HEADER_TD_CSS_SELECTOR)
        # header = "\n".join([th.get_text() + td.get_text() for th, td in zip(header_ths, header_tds)])
        # header = header if header else "None"

        # Get the post content
        contents = self.get_bs4_element(CONTENT_CSS_SELECTOR)
        if contents:
            content_buffer = []
            for bs4_element in contents.contents:
                if str(type(bs4_element)) == "<class 'bs4.element.NavigableString'>":
                    content_buffer.append(bs4_element.string)
                elif bs4_element.name not in ["font", "span", "div"]:
                    content_buffer.append(bs4_element.get_text())
            content = "".join(content_buffer)
        else:
            content = "None"

        return "<题目> " + post_title + "\n\n<发表于> " + date + "\n\n<基本信息>\n" + "\n\n<本文>\n" + content


# Get user ID, password, bot token from '.env'
load_dotenv()
causw_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
COMMUNITY_URL = "https://sw.cau.ac.kr/core/program/programalllist?menuid=001004001004&searchallyn=Y"
POST_LINKS_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > div > p.t1 > a"
POST_TITLES_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > div > p.t1 > a"
POST_STATES_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > p > span"
DATE_CSS_SELECTOR = ""
HEADERS_CSS_SELECTOR = ""
CONTENT_CSS_SELECTOR = ""


if __name__ == "__main__":
    # Initialize a chrome driver for FenHan
    causw_chrome = CAUSWChrome()

    # Scrape the new post
    causw_chrome.scrape_posts(causw_bot_token, chat_ids)

    # Exit the chrome when ctrl+c pressed
    causw_chrome.driver.quit()
