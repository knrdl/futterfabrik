from bs4 import BeautifulSoup
import requests
import html

from feedgen import Feed

TITLE = 'srf.ch Audio'
DESCRIPTION = 'srf.ch Audio Sendungen'
HOMEPAGE = 'https://www.srf.ch/audio/'
FIELDS = [{
    'name': 'url',
    'title': 'URL',
    'type': 'url',
    'required': True,
    'placeholder': 'https://www.srf.ch/audio/...',
    'pattern': 'https://www.srf.ch/audio/.+'
}]


def generate(url: str):
    feed = Feed(
        title=url.removesuffix('/').rsplit('/', 1)[-1],
        site_url=url,
        description='SRF.CH Audio'
    )

    _ = html.escape

    page = requests.get(url).text
    ents = BeautifulSoup(page).findAll('div', {'class': ['episode-listing']})
    for ent in ents:
        title = ent.find('h4', {'class': 'media-caption__title media-caption__title--audio'}).text.strip()
        url = ent.find('a', {'class': 'medium__caption--link'}).get('href')
        feed.add_item(
            title=title,
            url=url,
            body=f'<a href="{_(url)}">Link</a>',
            unique_id=url
        )
    return feed
