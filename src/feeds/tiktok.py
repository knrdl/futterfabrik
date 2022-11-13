import html
import traceback

import requests
from bs4 import BeautifulSoup

from config import common_headers

from feedgen import Feed

TITLE = 'Tiktok'
HOMEPAGE = 'https://urlebird.com'
FIELDS = [{
    'name': 'account',
    'title': 'Tiktok Account',
    'type': 'text',
    'required': True
}]

_ = html.escape


def generate(account: str):
    feed = Feed(
        title=account.title(),
        site_url=f'https://urlebird.com/user/{account}/',
        description='Tiktok'
    )

    found_videos = set()
    src = requests.get(feed.site_url, headers=common_headers).text
    for post in BeautifulSoup(src).findAll('div', {'class': 'thumb wc'}):
        for link in post.findAll('a'):
            if url := link.get('href'):
                if url.startswith('https://urlebird.com/video/') and url not in found_videos:
                    found_videos.add(url)
                    try:
                        src_video = requests.get(url, headers=common_headers).text
                        soup_video = BeautifulSoup(src_video).find('video')
                        video_url = soup_video.get('src')
                    except:
                        traceback.print_exc()
                        video_url = None
                    feed.add_item(title=link.text or account.title(), url=video_url,
                                  body=f'<video src="{_(video_url)}"/>' if video_url else url, unique_id=url)
        if len(found_videos) >= 15:  # only handle 15 newest entries to keep response time manageable
            break

    return feed
