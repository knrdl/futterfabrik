from bs4 import BeautifulSoup
import requests

from feedgen import Feed

TITLE = 'Motatos'
HOMEPAGE = 'https://www.motatos.de/neu-im-shop'

def generate():
    feed = Feed(
        title='Motatos',
        site_url=HOMEPAGE,
        description='Motatos - Neu im Shop'
    )

    soup = BeautifulSoup(requests.get(HOMEPAGE).text)
    for item in soup.find('div', {'class': "product-list"}).find('ul').find_all('li'):
        link = item.find('a')
        url = 'https://www.motatos.de' + link.get('href')
        title = link.find('span', {'class': 'label'}).text
        price = link.find('div', {'class': 'product-item-price'}).text.removesuffix('*')

        feed.add_item(title=f'{title} ({price})', body=link.text, url=url, unique_id=url)
    return feed
