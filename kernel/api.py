#.-.coding=utf8

__author__ = 'wangguodong'

import collectors
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
import json
from django.core import serializers

class APIError(Exception):
    _ERROR_MESSAGE_DICT = {
        0: "Success!",
        1: "Collector not found.",
        2: "Hey,you don't have the right key!",
        3: "TimeFormatError: Timestamp should be YYYYMMDDHHMMSS",
        4: "TimeValueError: Timestamp should be logical.",
        5: "Result is EMPTY!",
        6: "API SPECIFIC ERROR MESSAGE",
        9: "Failure! Please contact administrator.",
    }
    code = 0
    message = _ERROR_MESSAGE_DICT[0]
    def __init__(self, code):
        self.code = code
        self.message = self._ERROR_MESSAGE_DICT[self.code]
    def __str__(self):
        return self.message

# http://localhost:8000/api/weiqi/timeline.json?key=iamthekey&begin_time=20000101112233&end_time=20160101112233
def json_response(request, collector):
    json_dic = {}
    try:
        all_collectors = collectors.find_collector(collector)
        if not len(all_collectors) == 1:
            raise APIError(1)

        key = request.GET.get('key', '')
        _check_api_key(key)

        begin_time = request.GET.get('begin_time', '')
        begin_time = _check_time(begin_time)
        end_time = request.GET.get('end_time', '')
        end_time = _check_time(end_time)

        data = all_collectors[0].data(request, begin_time, end_time)
        _check_data(data)

        success = APIError(0)
        json_dic['code'] = success.code
        json_dic['message'] = success.message
        json_dic['results'] = data
    except APIError, e:
        json_dic['code'] = e.code
        json_dic['message'] = e.message
    except Exception, e:
        print str(e)
        json_dic['code'] = 6
        json_dic['message'] = e.message

    return HttpResponse(json.dumps(json_dic, ensure_ascii=False), 'application/json')

def _check_api_key(key):
    if not key == settings.TIMELINE_API_KEY:
        raise APIError(2)

def _check_time(time_to_check):
    if time_to_check == '':
        return datetime.now()
    if not len(time_to_check) == 14:
        raise APIError(3)
    try:
        return datetime.strptime(time_to_check,'%Y%m%d%H%M%S')
    except ValueError:
        raise APIError(4)

def _check_data(data):
    if data is None or len(data) == 0:
        raise APIError(5)