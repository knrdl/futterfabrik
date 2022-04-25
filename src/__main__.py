#!/usr/bin/env python3
from http import server
import socketserver
import traceback
from urllib.parse import urlsplit, parse_qsl

from feeds import feed_list, get_feed_module
from overview import gen_overview


class FeedHandler(server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def send(self, content: str, code: int, mime: str):
        content = content.encode('utf8')
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        try:
            query_line = self.path.strip() or '/'
            url = urlsplit(query_line)
            if url.path == '/':
                return self.send(gen_overview(), code=200, mime='text/html')
            else:
                if url.path.endswith('.rss') or url.path.endswith('.json'):
                    feed_name = url.path.rsplit('.')[0].removeprefix('/')
                    if feed_name in feed_list:
                        mod = get_feed_module(feed_name)
                        params = dict(parse_qsl(url.query))
                        feed = getattr(mod, 'generate')(**params)
                        if url.path.endswith('.rss'):
                            return self.send(feed.as_rss(), code=200, mime='application/rss+xml; charset=utf-8')
                        else:
                            return self.send(feed.as_json_feed(), code=200, mime='application/feed+json; charset=utf-8')
            return self.send('404 not found', code=404, mime='text/plain')
        except Exception as e:
            traceback.print_exc()
            return self.send(str(e), code=500, mime='text/plain')

    def version_string(self):  # overwrite Server response header
        return 'Futterfabrik'


class FeedServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


server = FeedServer(('', 80), FeedHandler)
print('Starting server on port 80')
server.serve_forever()
