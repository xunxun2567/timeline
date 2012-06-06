#.-.coding=utf8
__author__='xukaifang'

from django.shortcuts import render_to_response
from django.http import HttpResponse
from kernel.models import Object, Attribute
from django.db import models
import datetime
from django.utils import timezone
import collectors
import json
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

#http://localhost:8000/api?key=timeline&c=nike&c=nike&prev_update=20110101112233&init=0
JSON_RETURN_HEAD={0:'Success',
                  1:'Unknown Error',
                  2:'No collectors found',
                  3:'Key error or no key found',
                  4:'Required time is still in future'
                    }
def get_json_return_head(returnValue=0):
    return {'message':returnValue,
            'description':JSON_RETURN_HEAD[returnValue],
            'return_time':timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def json_api(request):
    content=request.GET
    content=content.copy()
    json_return=get_json_return_head(0)

    #check the API key
    key_GET=content.get('key')
    if (not key_GET) or key_GET!='timeline':
        json_return=get_json_return_head(3)
        return HttpResponse(json.dumps(json_return,ensure_ascii=False))

    #check the collectors
    collectors_GET=content.getlist('c')
    if collectors_GET:
        collectors_required=[]
        for collector in collectors_GET:
            collectors_required=collectors_required+collectors.find_collector(name=collector,package='shopping')
        collectors_required=list(set(collectors_required))
        if not collectors_required:
            json_return=get_json_return_head(2)
            return HttpResponse(json.dumps(json_return,ensure_ascii=False))
    else:
        collectors_required=collectors.find_collector(package='shopping')

    #Check the time
    time_GET=content.get('prev_update')
    time_required=timezone.now()
    if time_GET:
        time_required=datetime.datetime.strptime(time_GET,'%Y%m%d%H%M%S')

    #To see if the required time is in future.Right now it is forbidden to use the time not yet arrived
    if time_required>timezone.now():
        json_return=get_json_return_head(4)
        return HttpResponse(json.dumps(json_return,ensure_ascii=False))
    json_return['previous_update_time']=time_required.strftime('%Y-%m-%d %H:%M:%S')

    #Check if init, if init is mentioned, return info in the last 14 days
    init=content.get('init')
    TIME_FILTER=14
    if init:
        time_required=timezone.now()-datetime.timedelta(days=TIME_FILTER)
    elif time_required<timezone.now()-datetime.timedelta(days=TIME_FILTER):
        time_required=timezone.now()-datetime.timedelta(days=TIME_FILTER)

    #Get the information
    info={}
    for collector in collectors_required:
        info[collector.__class__.__name__]=[]
        objects=Object.objects.filter(branch=collector.__class__.__name__)

        objects=objects.filter(time__gt=time_required)

        #for test, only return 10 object for one collector
        for object in objects[:10]:
            object_value={}
            object_value['title']=object.title
            object_value['time']=object.time.strftime('%Y-%m-%d %H:%M:%S')
            object_value['url']=object.url
            attributes=Attribute.objects.filter(object=object)
            for attribute in attributes:
                object_value[attribute.name]=attribute.value
            info[collector.__class__.__name__].append(object_value)

    json_return['content']=info

    return HttpResponse(json.dumps(json_return,ensure_ascii=False))
    
        
            


