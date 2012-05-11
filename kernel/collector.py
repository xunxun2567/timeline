import django.dispatch
from django.dispatch import receiver
from models import Object, Attribute
import pkgutil
import collectors

object_found = django.dispatch.Signal(providing_args=["time", "title", "url", "check"])

@receiver(object_found)
def create_object(sender, title, url, time, check=True, **kwargs):
    title = title
    url = url
    time = time
    if not (check and Object.objects.filter(url=url).exists()):
        print sender.__class__.__name__
        new_object = Object(
            title = title,
            url = url,
            time = time,
            branch = sender.__class__.__name__,
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

class Collector(object):
    def fetch(self):
        print 'Default implementation of fetch, do nothing.'

def import_all_collectors():
    for module_name in [name for _, name, _ in pkgutil.walk_packages(collectors.__path__, collectors.__name__ + '.')]:
        __import__(module_name)