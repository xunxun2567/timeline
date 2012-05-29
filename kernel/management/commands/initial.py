__author__ = 'xukaifang'

from django.core.management import BaseCommand
import collectors

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) > 0:
            name = args[0]
        else:
            name = ''
        all_collectors = collectors.find_collector(name)
        if len(all_collectors) > 1:
            print 'Please choose only one collector from below to run.'
            print

            for collector in all_collectors:
                    print collector.__class__.__name__
            return

        if len(all_collectors) == 0:
            print 'no match collector'
            all_collectors = collectors.find_collector()
            print 'Please choose only one collector from below to run.'
            print

            for collector in all_collectors:
                print collector.__class__.__name__
            return

        if len(all_collectors) == 1:
            all_collectors[0].init()

