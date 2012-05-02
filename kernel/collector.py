import django.dispatch
from django.dispatch import receiver
from models import Object
import pkgutil
import collectors

object_found = django.dispatch.Signal(providing_args=["time", "title", "url"])

@receiver(object_found)
def create_object(sender, title, url, time, **kwargs):
    title = title
    url = url
    time = time
    if not Object.objects.filter(url=url).exists():
        new_object = Object(
            title = title,
            url = url,
            time = time,
            branch = sender.__class__.__name__,
        )
        new_object.save()

class Collector(object):
    def fetch(self):
        print 'Default implementation of fetch, do nothing.'
        pass

def import_all_collectors():
    for module_name in [name for _, name, _ in pkgutil.walk_packages(collectors.__path__, collectors.__name__ + '.')]:
        __import__(module_name)