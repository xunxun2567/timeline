__author__ = 'konglingkai'

import logging, datetime, os
import datetime
from django.utils import timezone
from django.conf import settings
from django import dispatch
from kernel.models import Object, Attribute

object_found = dispatch.Signal(providing_args=["time", "title", "url", "check"])

@dispatch.receiver(object_found)
def create_object(sender, title, url, time, check=True, **kwargs):
    title = title
    url = url
    time = time
    if time is None or len(str(time)) < 1:
        time = datetime.datetime.now()

    if not (check and Object.objects.filter(url=url).exists()):
        new_object = Object(
            title = title,
            url = url,
            time = time,
            added_time=timezone.now(),       #add the current time
            branch = sender.__class__.__name__,
        )
        new_object.save()

        for key in kwargs:
            if key == 'signal': continue
            attr = Attribute(
                object = new_object,
                name  = key,
                value = kwargs[key]
            )
            attr.save()

class CollectorLogHandler(logging.FileHandler):
    def __init__(self, collector_class=None):
        today = datetime.datetime.now().strftime('%Y_%m_%d')
        directory_name = os.path.join(settings.COLLECTOR_LOGGING_ROOT, today)
        if not os.path.exists(directory_name):
            os.mkdir(directory_name)
        if not collector_class:
            name = 'daily'
        else:
            name = collector_class.__name__

        filename = os.path.join(directory_name, name + '.txt')
        logging.FileHandler.__init__(self, filename, mode='a', encoding='utf-8')

class CollectorException(Exception):
    pass

class BaseCollector(object):
    object_fields=['time', 'title', 'url']
    attribute_fields=[]

    def __init__(self):
        handler = CollectorLogHandler(self.__class__)
        handler.setFormatter(logging.Formatter(fmt='[%(levelname)s] %(asctime)s: %(message)s'))
        console_handler = logging.StreamHandler()
        logger = logging.Logger(self.__class__.__name__, level=logging.DEBUG)
        logger.addHandler(console_handler)
        logger.addHandler(handler)
        self.logger = logger

    def fetch(self):
        raise CollectorException('fetch not implemented')

    def data(self, request, begin_time, end_time):
        controller_name = self.__class__.__name__
        objects = Object.objects.filter(branch=controller_name, time__gte=begin_time, time__lte=end_time).order_by('-time')[:50]

        results_list = []
        for a_object in objects.values():
            a_object_dic = {}
            for k,v in a_object.iteritems():
                print str(k)
                if k in self.object_fields:
                    if isinstance(v, datetime.datetime):
                        a_object_dic[str(k)] = v.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        a_object_dic[str(k)] = v

            attributes = Attribute.objects.filter(object_id=a_object['id'])
            a_attribute_dic = {}
            for a_attribute in attributes:
                if a_attribute.name in self.attribute_fields:
                    a_attribute_dic[a_attribute.name] = a_attribute.value
            a_object_dic['attributes'] = a_attribute_dic

            results_list.append(a_object_dic)

        return results_list


