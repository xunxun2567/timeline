__author__ = 'admin'

import collectors
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse

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

# http://localhost:8000/api/collector/timeline.json?key=111111&begin_date=20000101112233444&end_date=20160101112233444
def json(request, collector):
    json_dic = {}
    try:
        all_collectors = collectors.find_collector(collector)
        if not len(all_collectors) == 1:
            raise APIError(1)

        key = request.GET.get('key', '')
        _check_api_key(key)

        begin_date = request.GET.get('begin_date', '')
        begin_date = _check_date(begin_date)
        end_date = request.GET.get('end_date', '')
        end_date = _check_date(end_date)

        results = all_collectors[0].api(request, begin_date, end_date)
        _check_results(results)

        json_dic['results'] = results
    except APIError, e:
        json_dic['code'] = e.code
        json_dic['message'] = e.message
    except Exception, e:
        json_dic['code'] = 6
        json_dic['message'] = e.message

    return HttpResponse(json.dumps(json_dic, 'application/json'))

def _check_api_key(key):
    if not key == settings.TIMELINE_API_KEY:
        raise APIError(2)

def _check_date(date_to_check):
    if date_to_check == '':
        return datetime.now()
    if not len(date_to_check) == 14:
        raise APIError(3)
    try:
        return datetime.strptime(date_to_check,'%Y%m%d%H%M%S')
    except ValueError:
        raise APIError(4)

def _check_results(results):
    if results is None or len(results) == 0:
        raise APIError(5)