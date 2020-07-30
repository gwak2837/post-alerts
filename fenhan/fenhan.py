import os
import sys
import time
import json
from dotenv import load_dotenv

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome


class FenHanChrome(Chrome):
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
        date = self.get_bs4_element(DATE_CSS_SELECTOR)
        date = date["title"] if date else "None"

        # Get the summary of the post
        header_ths = self.get_bs4_elements(HEADER_TH_CSS_SELECTOR)
        header_tds = self.get_bs4_elements(HEADER_TD_CSS_SELECTOR)
        header = "\n".join([th.get_text() + td.get_text() for th, td in zip(header_ths, header_tds)])
        header = header if header else "None"

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

        return "<题目> " + post_title + "\n\n<发表于> " + date + "\n\n<基本信息>\n" + header + "\n\n<本文>\n" + content


# Get user ID, password, bot token from '.env'
load_dotenv()
fenhan_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
COMMUNITY_URL = "http://bbs.icnkr.com/forum.php?mod=forumdisplay&fid=1603&filter=author&orderby=dateline&sortid=344"
POST_LINKS_CSS_SELECTOR = "#separatorline ~ tbody > tr > th > a.s.xst"
POST_TITLES_CSS_SELECTOR = POST_LINKS_CSS_SELECTOR
TD_CSS_SELECTOR = "#postlist > div:nth-of-type(1) > table > tbody > tr:first-child > td:nth-child(2)"
DATE_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pi > div.pti > div.authi > em > span"
HEADERS_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pct > div.pcb > div.typeoption > table > tbody > tr"
CONTENT_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pct > div.pcb > div.t_fsz > table > tbody > tr > td"
HEADER_TH_CSS_SELECTOR = HEADERS_CSS_SELECTOR + " > th"
HEADER_TD_CSS_SELECTOR = HEADERS_CSS_SELECTOR + " > td"
COMMENTS_CSS_SELECTOR = ""


if __name__ == "__main__":
    # Initialize a chrome driver for FenHan
    fenhan_chrome = FenHanChrome()

    # Scrape the new post
    fenhan_chrome.scrape_posts(fenhan_bot_token, chat_ids)

    # Exit the chrome when ctrl+c pressed
    fenhan_chrome.driver.quit()
