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
    date = get_elements(DATE_CSS_SELECTOR)[0].attrs["title"]

    try:
        headers = get_elements(HEADER_CSS_SELECTOR, 10)[0].contents
        header_buffer = []
        for header in headers:
            if str(type(header)) == "<class 'bs4.element.Tag'>":
                header_buffer.append(header.th.text + header.td.text)
        header = "\n".join(header_buffer)
    except IndexError:
        print("No post header.")
        header = "None"

    try:
        contents = get_elements(CONTENT_CSS_SELECTOR, 10)[0].contents
        content_buffer = []
        for content in contents:
            if str(type(content)) == "<class 'bs4.element.NavigableString'>" and content != "\n":
                content_buffer.append(content.strip("\n "))
        content = "\n".join(content_buffer)
    except IndexError:
        print("No post content.")
        content = "None"

    return "题目: " + title + "\n\n发表于: " + date + "\n\n基本信息:\n" + header + "\n\n本文:\n" + content


# Get user ID, password, bot token from '.env'
load_dotenv()
fenhan_bot_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Initialize constants and a variable
POSTS_URL = "http://bbs.icnkr.com/forum.php?mod=forumdisplay&fid=1603&filter=author&orderby=dateline&sortid=344"
TITLES_CSS_SELECTOR = "#separatorline ~ tbody > tr > th > a.s.xst"
TD_CSS_SELECTOR = "#postlist > div:nth-of-type(1) > table > tbody > tr:first-child > td:nth-child(2)"
DATE_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pi > div.pti > div.authi > em > span"
HEADER_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pct > div.pcb > div.typeoption > table > tbody"
CONTENT_CSS_SELECTOR = TD_CSS_SELECTOR + " > div.pct > div.pcb > div.t_fsz > table > tbody > tr > td"

# Get the latest title of post
driver.get(POSTS_URL)

# Scrape the new post
scrape_posts(POSTS_URL, "", TITLES_CSS_SELECTOR, fenhan_bot_TOKEN, get_message)

# Exit the chrome when ctrl+c pressed
driver.quit()
