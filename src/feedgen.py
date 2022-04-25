import json

import feedgenerator


class Feed:
    def __init__(self, *, title: str, description: str = '', site_url: str):
        self.title = title
        self.description = description
        self.site_url = site_url
        self.items = []

    def add_item(self, unique_id: str, body: str, url: str, title: str):
        self.items.append({'id': unique_id, 'body': body, 'url': url, 'title': title})

    def as_json_feed(self) -> str:
        return json.dumps({
            "version": "https://jsonfeed.org/version/1.1",
            "title": self.title,
            "description": self.description,
            "home_page_url": self.site_url,
            "items": [
                {'id': item['id'], 'content_html': item['body'], 'url': item['url'], 'title': item['title']}
                for item in self.items
            ]
        }, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

    def as_rss(self) -> str:
        feed = feedgenerator.Rss201rev2Feed(title=self.title, link=self.site_url, description=self.description)

        for item in self.items:
            feed.add_item(title=item['title'], description=item['body'], link=item['url'], unique_id=item['id'])

        return feed.writeString('utf8')
