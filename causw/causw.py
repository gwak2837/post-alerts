import os
import sys
import time
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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
                return [
                    (post_link["href"][1:], post_title.get_text().strip() + " " + post_state.get_text().strip())
                    for post_link, post_title, post_state in zip(post_links, post_titles, post_states)
                ]

    def get_message_from(self, post_link, post_title):
        # Go to the post details page
        if not self.go_to_page(BASE_URL + post_link):
            return "Fail to get a message with post details"

        # Get the post summary
        post_trs = self.get_bs4_elements(POST_CSS_SELECTOR)
        if post_trs:
            company_name = post_trs[0].td.get_text().strip()
            progress_period = post_trs[1].td.get_text().strip()
            application_period = post_trs[2].td.get_text().strip()
            place_of_work = post_trs[3].td.get_text().strip()
            attachment = post_trs[4].td.get_text().strip()
            header_buffer = [
                f"기업명 : {company_name}",
                f"진행기간 : {progress_period}",
                f"신청기간 : {application_period}",
                f"근무장소 : {place_of_work}",
                f"첨부 : {attachment}",
            ]
            header = "\n".join(header_buffer)
        else:
            header = "None"

        # Get the post content
        content = self.get_bs4_element(CONTENT_CSS_SELECTOR)
        content = content.get_text().strip() if content else "None"

        return "<제목> " + post_title + "\n\n<요약>\n" + header + "\n\n<내용>\n" + content


# Get user ID, password, bot token from '.env'
load_dotenv()
causw_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_ids = set(json.loads(os.getenv("CHAT_IDs")))

# Initialize constants
BASE_URL = "https://sw.cau.ac.kr/core/program"
COMMUNITY_URL = "https://sw.cau.ac.kr/core/program/programalllist?menuid=001004001004&searchallyn=Y"
POST_LINKS_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > div > p.t1 > a"
POST_TITLES_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > div > p.t1 > a"
POST_STATES_CSS_SELECTOR = "#iph_content > div > div.list_type_mh1.mob_view.mt3 > ul > li > p > span"

POST_CSS_SELECTOR = "#programForm > div > div.view_type_h1.mt3 > table > tbody > tr:not(:last-child)"
CONTENT_CSS_SELECTOR = "#programForm > div > div.view_type_h1.mt3 > table > tbody > tr:last-child > td"


if __name__ == "__main__":
    # Initialize a chrome driver for FenHan
    causw_chrome = CAUSWChrome()

    # Scrape the new post
    causw_chrome.scrape_posts(causw_bot_token, chat_ids)

    # Exit the chrome when ctrl+c pressed
    causw_chrome.driver.quit()
