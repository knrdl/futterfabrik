import html
from datetime import datetime, timedelta, date
from urllib.parse import quote_plus

from bs4 import BeautifulSoup
import requests
import hashlib
import re

from feedgen import Feed

TITLE = 'Demos Berlin'
HOMEPAGE = 'https://www.berlin.de/polizei/service/versammlungsbehoerde/versammlungen-aufzuege/'
FIELDS = [{
    'name': 'days',
    'title': 'Demos innerhalb der nächsten',
    'info': 'Tage',
    'type': 'number',
    'default': '3',
    'min': 0,
    'required': True
}]

_ = html.escape


def generate(days: str):
    feed = Feed(
        title='Demos Berlin',
        site_url=HOMEPAGE,
        description='Demos Berlin'
    )
    days = timedelta(days=int(days))

    soup = BeautifulSoup(requests.get(HOMEPAGE).text)
    table = soup.find('table', {'class': "result"})
    if table:
        for ent in table.find('tbody').findAll('tr'):
            if ent.find('td', colspan="7"):
                continue
            demo_date = ent.find('td', headers='Datum').text.strip()
            demo_begin = ent.find('td', headers='Von').text.strip()
            demo_end = ent.find('td', headers='Bis').text.strip()
            demo_topic = ent.find('td', headers='Thema').text.strip()
            demo_zip = ent.find('td', headers='PLZ').text.strip()
            demo_location = ent.find('td', headers='Versammlungsort').text.strip()
            demo_route = ent.find('td', headers='Aufzugsstrecke').text.strip()
            date_obj = datetime.strptime(demo_date, '%d.%m.%Y')
            today = date.today()
            today = datetime(today.year, today.month, today.day)
            if date_obj >= today and date_obj - today <= days:
                if demo_location or demo_zip:
                    location_slug = f"{demo_location} {demo_zip}"
                    location_text = f'''
                        <li>
                            <a href="https://www.openstreetmap.org/search?query={quote_plus(location_slug)}">
                                {_(location_slug)}
                            </a>
                        </li>
                    '''
                else:
                    location_text = ''
                unique_id = hashlib.md5(f'{demo_date}-{demo_begin}-{demo_end}-{demo_topic}'.encode('utf8')).hexdigest()
                feed.add_item(title=demo_topic,
                              body=re.sub(r'\s+', ' ', f'''
                                    <ul>
                                    <li><b>{_(demo_topic)}</b></li>
                                    <li>📅 {_(demo_date)} {_(demo_begin)} - {_(demo_end)}</li>
                                    {location_text}
                                    <li>{_(demo_route)}</li>
                                    </ul>
                                '''),
                              url=feed.site_url,
                              unique_id=unique_id)
    return feed
