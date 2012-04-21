from django.shortcuts import  render_to_response
import collector

def home (request):
    return render_to_response('home.html')

def find_collector(collector_id):
    collector.import_all_collectors()
    all_collectors = collector.Collector.__subclasses__()
    collectors_found = []
    for collector_class in all_collectors:
        if collector_id != "" and collector_class.__name__.lower().find(collector_id.lower()) == -1:
            continue
        the_collector = collector_class()
        collectors_found.append(the_collector)
    return collectors_found

def pull (request, collector_id):
    """
    pull the objects from the collectors
    """
    for c in find_collector(collector_id):
        c.pull()

    return render_to_response('pull.html')

def clone (request, collector_id):
    """
    initial cloning of the objects
    """
    for c in find_collector(collector_id):
        c.clone()

    return render_to_response('clone.html')