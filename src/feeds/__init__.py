import importlib
import os
from glob import glob

_py_files = [os.path.basename(mod)[:-3] for mod in glob(f'{os.path.dirname(os.path.realpath(__file__))}/*.py')]
feed_list = sorted([pyfile for pyfile in _py_files if not pyfile.startswith('_')])


def get_feed_metadata(name: str):
    if name not in feed_list:
        raise Exception('unknown feed')
    mod = importlib.import_module('.' + name, 'feeds')
    return {
        'id': name,
        'title': getattr(mod, 'title') if hasattr(mod, 'title') else name.title(),
        'description': getattr(mod, 'description') if hasattr(mod, 'description') else '',
        'fields': getattr(mod, 'fields') if hasattr(mod, 'description') else []
    }


from . import *
