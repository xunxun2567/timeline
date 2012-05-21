__author__ = 'konglingkai'

import pkgutil

# auto import every modules under this package
[__import__(name) for _, name, _ in pkgutil.walk_packages(__path__, __name__ + '.')]

from kernel.collector import BaseCollector

def find_collector(name=''):
    collectors = [_class() for _class in BaseCollector.__subclasses__()]
    match = []
    for collector in collectors:
        if collector.__class__.__name__.lower().find(name.lower()) != -1:
            match.append(collector)

    return match;