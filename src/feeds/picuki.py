import html

import requests
from bs4 import BeautifulSoup
from feedgen import Feed

TITLE = 'Picuki'
DESCRIPTION = 'Instagram Viewer'
HOMEPAGE = 'https://www.picuki.com/'
FIELDS = [{
    'name': 'account',
    'title': 'Instagram Account',
    'type': 'text',
    'required': True
}]

_ = html.escape


def generate(account: str):
    feed = Feed(
        title=account.title(),
        site_url=f'https://www.picuki.com/profile/{account}',
        description='Instagram (Picuki)'
    )

    src = requests.get(feed.site_url).text

    for post in BeautifulSoup(src).find('ul', {'class': 'profile-box-photos'}).findChildren("li", recursive=False):
        if img := post.find('img', {'class': 'post-image'}):
            if img_url := img.get('src'):
                url = post.find('div', {'class': 'box-photo'}).find('a').get('href')
                desc = (post.find('div', {'class': 'photo-description'}).text or '').strip()
                location = (post.find('div', {'class': 'photo-location'}).text or '').strip()
                if location:
                    desc += f' ({location})'
                feed.add_item(title=account.title(), url=url, body=f'<img src="{_(img_url)}"/><p>{_(desc)}</p>',
                              unique_id=url)
    return feed
