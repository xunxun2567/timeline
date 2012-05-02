__author__ = 'konglingkai'

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = 'list the status of the current collector'

    def handle(self, *args, **options):
        print args
        pass