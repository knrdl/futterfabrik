import json
from datetime import datetime

import requests

from feedgen import Feed

TITLE = 'getnext.to'
HOMEPAGE = 'https://de.getnext.to'
FIELDS = [{
    'name': 'profile',
    'title': 'Profil Name',
    'type': 'text',
    'required': True
}]


def generate(profile: str):
    feed = Feed(
        title=profile.title(),
        site_url=f'https://de.getnext.to/{profile}',
        description='getnext.to'
    )

    src = requests.get(feed.site_url).text
    src = src.split('window.__NUXT__=')[1].split(';</script>')[0]
    dat = json.loads(src)
    for post in dat['state']['artist']['stickyPosts']:
        feed.add_item(
            title=post['title'],
            url=f"https://de.getnext.to/{profile}/post/{post['titleSlug']}/{post['_id']}",
            body=post['post'],
            unique_id=post['_id'],
            published=datetime.fromisoformat(post['publishDateTime'].replace('Z', '+00:00'))
        )
    return feed
