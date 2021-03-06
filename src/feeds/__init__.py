import importlib
import os
from glob import glob
from types import ModuleType

_py_files = [os.path.basename(mod)[:-3] for mod in glob(f'{os.path.dirname(os.path.realpath(__file__))}/*.py')]
feed_list = sorted([pyfile for pyfile in _py_files if not pyfile.startswith('_')])


def get_feed_module(name: str) -> ModuleType:
    if name not in feed_list:
        raise Exception('unknown feed')
    return importlib.import_module('.' + name, 'feeds')


def get_feed_metadata(name: str):
    mod = get_feed_module(name)
    return {
        'name': name,
        'homepage': getattr(mod, 'HOMEPAGE') if hasattr(mod, 'HOMEPAGE') else '',
        'title': getattr(mod, 'TITLE') if hasattr(mod, 'TITLE') else name.title(),
        'description': getattr(mod, 'DESCRIPTION') if hasattr(mod, 'DESCRIPTION') else '',
        'fields': getattr(mod, 'FIELDS') if hasattr(mod, 'FIELDS') else []
    }


for feed_name in feed_list:
    mod = get_feed_module(feed_name)
    if not hasattr(mod, 'generate') or not callable(getattr(mod, 'generate')):
        raise Exception('module "%s" does not include the required generate function' % feed_name)
