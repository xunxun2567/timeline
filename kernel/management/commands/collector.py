__author__ = 'konglingkai'

from django.core.management import BaseCommand
from kernel.models import Object,Attribute
import datetime
import collectors

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) == 0:
            print 'select a collector below:'
            print
            for collector in collectors.find_collector():
                print collector.__class__.__name__
            return

        collector_name = args[0]

        result = collectors.find_collector(collector_name)
        if len(result) == 0:
            print 'no collectors found:'
            print
            for collector in collectors.find_collector():
                print collector.__class__.__name__
            return

        if len(result) > 1:
            print 'please select only one collector'
            print
            for collector in result:
                print collector.__class__.__name__
            return

        collector = result[0]
        print collector.__class__.__name__

        objects = Object.objects.filter(branch=collector.__class__.__name__)
        print 'total objects: %d' % len(objects)

        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        today_objects = objects.filter(time__gt=yesterday)
        print 'objects found later than %s: %d' % (yesterday.strftime('%Y-%m-%d'), len(today_objects))
        today_objects = today_objects[:100]
        for obj in today_objects:
            obj.dump()




