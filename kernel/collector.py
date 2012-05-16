__author__ = 'konglingkai'

import logging, datetime, os
from django.conf import settings
from django import dispatch
from kernel.models import Object, Attribute

object_found = dispatch.Signal(providing_args=["time", "title", "url", "check"])

@dispatch.receiver(object_found)
def create_object(sender, title, url, time, check=True, **kwargs):
    title = title
    url = url
    time = time
    if not (check and Object.objects.filter(url=url).exists()):
        new_object = Object(
            title = title,
            url = url,
            time = time,
            line = sender.__class__.__name__,
        )
        new_object.save()

        for key in kwargs:
            if key == 'signal': continue
            attr = Attribute(
                obj = new_object,
                key = key,
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


