title = 'ebay Kleinanzeigen'
description = 'Feed für neue Suchergebnisse'
fields = [{
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
    'min': '0',
    'info': 'Kilometer'
}]


def generate(search, location, radius=''):
    print('search', search, 'location', location, 'radius', radius)
    return 'blub'  # todo
