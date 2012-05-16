__author__ = 'konglingkai'

from django.core.management import BaseCommand
import collectors

class Command(BaseCommand):
    def handle(self, *args, **options):
        for collector in collectors.find_collector():
            print collector.__class__.__name__
