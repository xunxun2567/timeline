from django.shortcuts import  render_to_response
import collector

def home (request):
    return render_to_response('home.html')


def pull (request):
    """
    pull the objects from the collectors
    """
    collector.import_all_collectors()

    all_collectors = collector.Collector.__subclasses__()
    for collector_class in all_collectors:
        the_collector = collector_class()
        the_collector.pull()

    return render_to_response('pull.html')

def clone (request):
    """
    initial cloning of the objects
    """
    collector.import_all_collectors()

    all_collectors = collector.Collector.__subclasses__()
    for collector_class in all_collectors:
        the_collector = collector_class()
        the_collector.clone()
    return render_to_response('clone.html')