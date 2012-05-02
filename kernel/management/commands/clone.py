__author__ = 'konglingkai'

from django.core.management.base import BaseCommand, CommandError
from kernel import collector

def find_collector(collector_id):
    collector.import_all_collectors()
    all_collectors = collector.Collector.__subclasses__()
    collectors_found = []
    for collector_class in all_collectors:
        if collector_id != "" and collector_class.__name__.lower().find(collector_id.lower()) == -1:
            continue
        the_collector = collector_class()
        collectors_found.append(the_collector)
    return collectors_found

class Command(BaseCommand):
    args = '<collector_id>'

    def handle(self, *args, **options):
        if len(args) == 0:
            collector_id = ''
        else:
            collector_id = args[0]

        for c in find_collector(collector_id):
            c.clone()