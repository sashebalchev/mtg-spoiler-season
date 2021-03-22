import datetime
import re
import time
import webbrowser

import praw
from win10toast import ToastNotifier

from config import config

REDDIT = praw.Reddit(client_id=config['CLIENT_ID'],
                     client_secret=config['CLIENT_SECRET'],
                     user_agent=config["USER_AGENT"])
BROWSER_PATH = config['BROWSER_PATH']
SUBREDDIT = config['SUBREDDIT']
posts = []
posts_names = []
toaster = ToastNotifier()

if __name__ == "__main__":
    while True:
        for submission in REDDIT.subreddit(SUBREDDIT).new(limit=10):
            if (submission.link_flair_text == config['SPOILER_FLAIR'] or re.match(r'\[([^\]]*)\]', submission.title)) and submission.title[6:].lower() not in posts_names:
                posts_names.append(submission.title[6:].lower())
                if not submission.is_self:
                    toaster.show_toast("New Spoiler", submission.title)
                    webbrowser.get(BROWSER_PATH).open(
                        f'https://www.reddit.com{submission.permalink}')
        time.sleep(60)
