#!/usr/bin/env python3
from http import server
import socketserver
import traceback
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
            path = self.path.strip() or '/'
            if path == '/':
                self.send(gen_overview(), code=200, mime='text/html')
            else:
                pass  # todo
        except Exception as e:
            traceback.print_exc()
            self.send(str(e), code=500, mime='text/plain')


class FeedServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


server = FeedServer(('', 80), FeedHandler)
print('Starting server on port 80')
server.serve_forever()
