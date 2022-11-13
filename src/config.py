import os

BASE_URL = os.getenv('BASE_URL', default='http://localhost')

common_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/106.0',
    'Referer': 'https://www.google.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',  # should not include br, as requests/urllib cannot handle it
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'TE': 'Trailers',
    'Upgrade-Insecure-Requests': '1'
}
