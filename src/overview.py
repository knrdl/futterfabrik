#!/usr/bin/env python3
import re
from collections import OrderedDict
from typing import Literal
from urllib.parse import urlencode

from jinja2 import Template
from feeds import feed_list, get_feed_metadata
from config import BASE_URL

with open('overview.jinja2') as f:
    template = Template(f.read())


def build_feed_url(feed_format: Literal['rss', 'json'], feed_metadata):
    query_string = urlencode(OrderedDict({field['name']: '' for field in feed_metadata['fields']}))
    return f"{BASE_URL}/{feed_metadata['name']}.{feed_format}?{query_string}"


def gen_overview():
    return re.sub(r'\r?\n\s*', ' ', template.render(
        feeds=[get_feed_metadata(feed) for feed in feed_list],
        build_feed_url=build_feed_url
    ))
