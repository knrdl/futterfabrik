from bs4 import BeautifulSoup
import requests
import html

from feedgen import Feed

TITLE = 'Motatos'
HOMEPAGE = 'https://www.motatos.de/neu-im-shop'

_ = html.escape

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
        pic_url = link.find('img').get('src')
        if pic_url:
            pic_url = pic_url.split('?')[0]
        info2 = link.find('span', {'class': 'brand-and-weight'}).text
        info3 = link.find('span', {'class': 'comparison-price'}).text

        feed.add_item(title=f'{title} ({price})', body=f'''
            <h1>{_(title)} ({_(price)})</h1>
            <p>{_(info2)} {_(info3)}</p>
            <img src="{_(pic_url)}">
        ''', url=url, unique_id=url)
    return feed
