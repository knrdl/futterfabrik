import sys
from bs4 import BeautifulSoup
import requests
import html
import os

from config import common_headers
from feedgen import Feed

TITLE = 'ebay Kleinanzeigen'
DESCRIPTION = 'Feed für neue Suchergebnisse'
HOMEPAGE = 'https://www.ebay-kleinanzeigen.de'
FIELDS = [{
    'name': 'search',
    'title': 'Suchbegriff',
    'type': 'text',
    'required': True,
}, {
    'name': 'location',
    'title': 'Ort',
    'type': 'text',
    'required': True,
    'info': 'z.B. Berlin'
}, {
    'name': 'radius',
    'title': 'Suchradius',
    'type': 'number',
    'required': False,
    'min': 0,
    'info': 'Kilometer'
}]


def location_id(sess, location_term):
    res = sess.get('https://www.ebay-kleinanzeigen.de/s-ort-empfehlungen.json?query=%s' % location_term,
                   headers=common_headers)
    assert res.ok, res.text
    loc_id = list(res.json().keys())[0].replace('_', '')
    return loc_id


def fetch_page(sess, loc_id, *, search='', page=1, radius=None):
    if search:
        search = search.lower().replace(" ", "-")
        url = f'https://www.ebay-kleinanzeigen.de/s-walled-garden/seite:{page}/{search}/k0l{loc_id}'
    else:
        url = f'https://www.ebay-kleinanzeigen.de/s-walled-garden/seite:{page}/l{loc_id}'
    url = url.replace('/seite:1/', '/')
    if radius:
        url += f'r{radius}'
    res = sess.get(url, headers=common_headers)
    assert res.ok, res.text
    return res.text


def parse_ad(ent):
    ad_id = (ent.find('article') or {}).get('data-adid')
    if ad_id:
        img_url = None
        img_div = ent.find('div', {'class': 'imagebox'})
        if img_div:
            img_url = img_div.get('data-imgsrc')
            if img_url:
                img_url = img_url.replace('$_2.JPG', '$_59.JPG')
        title = None
        title_div = ent.find('h2')
        if title_div:
            title = title_div.text.strip()
        price_div = ent.find('p', {'class': 'aditem-main--middle--price'}) or \
                    ent.find('p', {'class': 'aditem-main--middle--price-shipping--price'})
        if price_div:
            price = price_div.text.strip()
        else:
            price = '?'
        desc = None
        desc_div = ent.find('div', {'class': 'aditem-main'})
        if desc_div:
            desc_div = desc_div.find('p')
            if desc_div:
                desc = desc_div.text.strip()
        if not title:
            print('Skipping item:', ent, file=sys.stderr)
            return
        return dict(
            price=price, ad_id=ad_id, img_url=img_url, title=title, desc=desc,
            link=f'https://www.ebay-kleinanzeigen.de/s-anzeige/walled-garden/{ad_id}'
        )


def has_next_page(soup):
    elem = soup.find('span', {'class': 'pagination-current'})
    if not elem:
        return False
    items = list(elem.next_siblings)
    return any((item != '\n' for item in items))


def make_session():
    sess = requests.Session()
    res = sess.get('https://www.ebay-kleinanzeigen.de', headers=common_headers)
    assert res.ok, res.text
    return sess


def get_ads(sess, loc_id, *, search='', radius=None, max_pages=2):
    page = 1
    while True:
        src = fetch_page(sess, loc_id, search=search, radius=radius, page=page)
        soup = BeautifulSoup(src)
        if ads_item := soup.find('ul', {'id': 'srchrslt-adtable'}):
            for ad_item in ads_item.findAll('li'):
                if ad := parse_ad(ad_item):
                    yield ad
            if not has_next_page(soup) or page > 50 or (max_pages and page >= max_pages):
                break
            page += 1
        else:
            break


def generate(search, location, radius=''):
    sess = make_session()
    loc_id = location_id(sess, location)
    feed = Feed(
        title=f'Ebay Kleinanzeigen ("{search.title()}" in {location.title()})',
        site_url=f'https://www.ebay-kleinanzeigen.de/s-walled-garden/{search}/k0l{loc_id}',
    )

    _ = html.escape

    for ad in get_ads(sess, loc_id, search=search, radius=radius):
        desc = ''
        if ad["desc"]:
            desc += f'<p>{_(ad["desc"]).replace(os.linesep, "<br>")}</p>'
        if ad["img_url"]:
            desc += f'<img src="{_(ad["img_url"])}">'
        feed.add_item(title=f"{ad['title']} ({ad['price']})", url=ad['link'], body=desc, unique_id=ad['ad_id'])

    return feed
