#!/usr/bin/env python3
import re
from jinja2 import Template
from feeds import feed_list, get_feed_metadata

with open('overview.jinja2') as f:
    template = Template(f.read())


def gen_overview():
    return re.sub(r'\r?\n\s*', '', template.render(feeds=[get_feed_metadata(feed) for feed in feed_list]))
