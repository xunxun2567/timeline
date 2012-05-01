__author__ = 'konglingkai'

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle_noargs(self, *args, **options):
        print 'status'