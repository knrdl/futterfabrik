import re

import requests
from bs4 import BeautifulSoup

from feedgen import Feed

TITLE = 'ARD Mediathek'
DESCRIPTION = 'Neue Folgen einer Sendung in der ARD Mediathek'
HOMEPAGE = 'https://www.ardmediathek.de'
FIELDS = [{
    'name': 'url',
    'title': 'URL der Seite zur Sendung',
    'type': 'url',
    'required': True,
    'pattern': 'https://www.ardmediathek.de/sendung/'
}]


def generate(url: str) -> Feed:
    url_prefix = 'https://www.ardmediathek.de/sendung/'
    if not url.startswith(url_prefix):
        raise Exception('URL must start with "%s"' % url_prefix)

    feed = Feed(
        title=re.sub(r'\W', r' ', re.sub('.*/sendung/([^/]+)/.*', r'\1', url).title()),
        site_url=url,
        description='ARD Mediathek'
    )

    for ent in BeautifulSoup(requests.get(url).text).findAll('a'):
        link = ent.get('href') or ''
        if link.startswith('/video/'):
            link = 'https://www.ardmediathek.de' + link
            title = ent.find('h3').text
            feed.add_item(title=title, body=feed.title, url=link, unique_id=link)

    return feed
