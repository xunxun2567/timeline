#.-.coding=utf8
__author__='xukaifang'

from django.shortcuts import render_to_response
from django.http import HttpResponse
from kernel.models import Object
from django.db import models
import datetime
from django.utils import timezone
import collectors
# Create your views here.
rn='<br>'

def one_day(request):
    return render_to_response('one_day.html')

def show(request):
    return HttpResponse("We are trying to show something here")

def view_today(request,collector_name):
    return view_someday(request,collector_name,time_filter=1)

def view_someday(request,collector_name,time_filter=1):
    collectors_matched=collectors.find_collector(collector_name)
    if len(collectors_matched)==0:
        http_response='<h1>Cannot find \"'+collector_name+'\"<br>'
        http_response+='Please select one from below:'+rn+'</h1>'
        http_response+='<p>'
        for collector in collectors.find_collector():
            class_name=collector.__class__.__name__
            link='<a href=\"http://localhost:8000/kernel/'+class_name+'/\">'+class_name+'</a>'
            http_response+=link+rn
        http_response+='</p>'
        return HttpResponse(http_response)

    elif len(collectors_matched)>1:
        http_response='<h1>'+str(len(collectors_matched))+' collectors have been found like \"'+collector_name+'\"<br>'
        http_response+='Please select one from below:'+rn+'</h1>'
        http_response+='<p>'
        for collector in collectors_matched:
            class_name=collector.__class__.__name__
            link='<a href=\"http://localhost:8000/kernel/'+class_name+'/\">'+class_name+'</a>'
            http_response+=link+rn
        http_response+='</p>'
        return HttpResponse(http_response)

    else:
        TIME_FILTER=int(time_filter)
        time_label='today'
        if TIME_FILTER>1:
            time_label='in the last %d days' %TIME_FILTER
        collector=collectors_matched[0]
        objects = Object.objects.filter(branch=collector.__class__.__name__)
        time_limit=timezone.now()-datetime.timedelta(days=TIME_FILTER)
        objects_today=objects.filter(time__gt=time_limit)
        if len(objects_today)==0:
            search_result='<p>No update '+time_label+' !!!</p>'
        else:
            search_result='<table border=\"1\"><tr><th>Title</th><th>Time</th><th>URL</th></tr>'
            for object in objects_today:
                search_result+='<tr><td>'\
                               +object.title\
                               +'</td><td>'+object.time.strftime('%Y-%m-%d %H:%M:%S')\
                               +'</td><td>'+'<a href=\"'+object.url+'\">'+object.url+'</a>'\
                               +'</td></tr>'
            search_result+='</table>'
                
        http_response='<h1>\"'+collector.__class__.__name__+'\" has the following object(s) updated '+time_label+' :</h1>'
        http_response+=search_result
        return HttpResponse(http_response)