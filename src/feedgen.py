import json
from datetime import datetime

import feedgenerator


class Feed:
    def __init__(self, *, title: str, description: str = '', site_url: str):
        self.title = title
        self.description = description
        self.site_url = site_url
        self.items = []

    def add_item(self, unique_id: str, body: str, url: str, title: str, published: datetime = None):
        self.items.append({'id': unique_id, 'body': body, 'url': url, 'title': title, 'pubdate': published})

    def as_json_feed(self) -> str:
        json_items = []
        for item in self.items:
            json_item = {'id': item['id'], 'content_html': item['body'], 'url': item['url'], 'title': item['title']}
            if item['pubdate']:
                json_item['date_published'] = item['pubdate'].isoformat()
            json_items.append(json_item)

        return json.dumps({
            "version": "https://jsonfeed.org/version/1.1",
            "title": self.title,
            "description": self.description,
            "home_page_url": self.site_url,
            "items": json_items
        }, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

    def as_rss(self) -> str:
        feed = feedgenerator.Rss201rev2Feed(title=self.title, link=self.site_url, description=self.description)

        for item in self.items:
            feed.add_item(title=item['title'], description=item['body'], link=item['url'], unique_id=item['id'],
                          pubdate=item['pubdate'])

        return feed.writeString('utf8')
