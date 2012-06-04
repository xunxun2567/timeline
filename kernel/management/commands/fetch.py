__author__ = 'konglingkai'

from django.core.management import BaseCommand
import collectors
from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-p',
            '--p',
            dest='package',
            default=False,
            help='run collectors in a certain package'),
        )

    def handle(self, *args, **options):

        print options
        if len(args) > 0:
            name = args[0]
        else:
            name = ''
        package = options['package']
        all_collectors = collectors.find_collector(name, package=package)


        if len(all_collectors) > 1 and package == False:
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

        for collector in all_collectors:
            try:
                collector.fetch()
            except Exception as ex:
                print ex

